from src.utils import *
from src.tools import *
from src.prompts import *
from src.database import *
from time import time


class ChatBot():
    def __init__(self, user_id) -> None:
        self.history = []
        self.id = user_id
        
    async def initialize(self):
        self.start_prompt = get_assistant_start()
        self.system_prompt = get_system_prompt()
        self.knowledge_prompt = get_knowledge_prompt()
        self.vision_prompt = get_vision_prompt()

        self.tools_dict = {
            "analyze_health_issue": self.search_knowledge,
            "provide_dynamic_health_knowledge": self.search_knowledge,
            "comprehensive_health_and_prevention_info_retrieval": self.search_knowledge
        }

        self.default_history = [self.system_prompt, self.start_prompt]
        self.histories = await self.initialize_history()
        
    async def initialize_history(self):
        histories = await read_history(self.id)
        threadList = histories.keys()  # histories is dictionary
        new_histories = {thread: [{key: chat[key] for key in chat if key not in ['user_id', 'cost', 'output_token', 'prompts', 'thread', 'date', 'attach', 'input_token','url']} for chat in histories[thread]] for thread in threadList}
        return new_histories if new_histories is not None else {}
    
    def initialize_chat(self,thread_id):
        self.history = self.histories[thread_id].copy()[1:] if self.histories.get(thread_id) is not None else self.default_history.copy()
        self.input_messages = []
        self.output_tokens = ""
        
    async def insert_chat(self, thread_id, suggestion, user_query, file_url, file_type, output, start_time ):
        end_now = time()
        self.histories[thread_id] = [[end_now, suggestion]] + self.history
        input_token = count_tokens_from_messages(self.input_messages, CHAT_MODEL)
        output_token = count_tokens_from_messages(self.output_tokens, CHAT_MODEL)
        input_cost = calculate_cost(input_token, True)
        output_cost = calculate_cost(output_token, False)
        document1 = {'user_id': self.id, 'thread':thread_id, 'role':'user', 'content':user_query, 'date':start_time, 'input_token':input_token, 'cost':input_cost, 'url':file_url, 'attach':file_type}
        await insert_chat(document1)
        document2 = {'user_id': self.id, 'thread':thread_id, 'role':'assistant', 'content':output, 'date':end_now, 'output_token':output_token, 'cost':output_cost, 'prompts':suggestion}
        await insert_chat(document2)
        
    async def search_knowledge(self, query, top_k=12):
        query_vector = await get_embedding(query)
        print('embedding done!')
        result = pindex.query(vector=query_vector, top_k=top_k)
        matches  = result.to_dict()['matches']
        ids = [match['id'] for match in matches]
        data = pindex.fetch(ids).to_dict()['vectors']
        response = [data[id]['metadata'] for id in ids]
        print(len(response))
        return json.dumps(response)
    
    async def chat(self, thread_id, user_query, file_url='', file_type=''):
        start_time = time()
        self.initialize_chat(thread_id)
        
        if file_url != '':
            self.history.append({"role": "user", "content": f"{file_type}_url: {file_url}\n question: {user_query}"})
            if file_url == 'pdf':
                extracted_text = await pdf_textract_froms3(file_url)
                user_prompt = get_user_vision_prompt_image_text(extracted_text, user_query)
            elif file_type == 'image':
                extracted_text = await textract_fromS3(file_url)
                user_prompt = get_user_vision_prompt_image_text(extracted_text, user_query)
            
            if len(self.history) <= 6:
                messages =  [self.system_prompt]+ self.history.copy() + [user_prompt]
            else:
                messages = [self.system_prompt] + self.history[-6:] + [user_prompt]
            messages.append(self.vision_prompt)
            
            self.input_messages += messages          
            response = await client.chat.completions.create(
                model=CHAT_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=4000,
                stream=True
            )
            output = ''
            async for chunk in response:
                data = chunk.choices[0].delta
                if hasattr(data, 'content') and data.content is not None:
                    output += data.content 
                    yield f"data: {json.dumps({'token': data.content})}\n\n".encode("utf-8")
            self.history.append({"role": "assistant", "content": output})
            self.output_tokens += output
        else:
            self.history.append({"role": "user", "content": user_query})
            if len(self.history) <= 5:
                messages = [self.system_prompt] + self.history.copy()
            else:
                messages = [self.system_prompt] + self.history[-5:]

            func_messages = self.history[-2:]
            self.input_messages += func_messages
            
            print('Start')
            
            function_response = await client.chat.completions.create(
                model=CHAT_MODEL,
                messages=func_messages,
                temperature=0,
                tools=tools,
                tool_choice='auto',
                stream=True
            )
            
            output = ""
            is_tool_call = False
            func_args = ""
            async for chunk in function_response:
                func_message = chunk.choices[0].delta
                content = func_message.content
                if content is None and func_message.tool_calls is not None:
                    if not is_tool_call: 
                        tool_calls = func_message.tool_calls
                        message = func_message
                    is_tool_call = True
                    func_args += func_message.tool_calls[0].function.arguments
                elif content is not None and not is_tool_call:
                    break
                
            print(func_args)
            
            if is_tool_call and message.role:
                for tool_call in tool_calls:
                    messages.append(message)
                    func_name = tool_call.function.name
                    print(func_name)
                    func_to_call = self.tools_dict[func_name]
                    print(func_name)
                    func_response = await func_to_call(func_args)
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": func_name,
                            "content": func_response
                        }
                    )
                messages.append(self.knowledge_prompt)
                
                self.input_messages += messages[:-3] + messages[-2:]
            else:
                self.input_messages += messages
            
            print('Answering')
            
            response = await client.chat.completions.create(
                model=CHAT_MODEL,
                messages=messages,
                temperature=0.7,
                stream=True,
                max_tokens=4000
            )
            
            output = ""
            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content is not None:
                    output += content
                    yield f"data: {json.dumps({'token': content})}\n\n".encode("utf-8")
                    
            self.output_tokens += output
            self.history.append({'role': 'assistant', 'content': output})
            print('Answered!')
            
        suggestion_prompt = get_suggestion_prompt(get_history_text(self.history[-4:]))
        self.input_messages.append(suggestion_prompt)

        suggestion_response = await client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[suggestion_prompt],
            temperature=0.7,
            max_tokens=100,
        )
        suggestion = suggestion_response.choices[0].message.content
        self.output_tokens += suggestion
        yield f"data: {json.dumps({'token': f'pr0mpt{suggestion}'})}\n\n".encode("utf-8")
        
        print('Done')
        await self.insert_chat(thread_id, suggestion, user_query, file_url, file_type, output, start_time)
        
    async def generate_summarize_text(self, thread_id):
        history_text = get_history_text(self.histories[thread_id][1:])
        messages = [get_summarization_prompt(history_text)]
        response = await client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2500,
        )
        return response.choices[0].message.content.replace('\n', '<br/>').replace('```html<br/>', '').replace('```', '').replace('<br/>', '')