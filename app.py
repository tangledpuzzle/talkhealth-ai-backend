import logging
from fastapi import FastAPI, HTTPException, Header, Request, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from src.bot import *
from src.models.request import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bots = {}

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://www.talkhealth.ai",
    "https://talkhealth.ai",
    "https://talkhealth-ai.vercel.app"
]

headers = {
    "Cache-Control": "no-cache",
    "Content-Type": "text/event-stream",
    "Transfer-Encoding": "chunked",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


async def validate_thread_id(request: Request, Authorization: str = Header(None)):
    # Extract the encrypted threadID from the Authorization header
    encrypted_thread_id = Authorization.split(" ")[1] if Authorization else None
    print(encrypted_thread_id)

    if not encrypted_thread_id:
        raise HTTPException(status_code=401, detail="Authorization header missing or malformed")

    try:
        decrypted_thread_id = decrypt(encrypted_thread_id)
        # Decrypt the threadID. Adjust the decryption method as per your requirement
        body = await request.json()
        if decrypted_thread_id != body.get("thread_id"):
            raise HTTPException(status_code=400, detail="Invalid thread ID")
    except Exception as e:
        # Generic exception handling; refine as needed
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/chat")
async def chat(chat_message: ChatMessage, validated: bool = Depends(validate_thread_id)):
    # bot = ChatBot()
    uid = chat_message.uid
    thread_id = chat_message.thread_id
    file_type = chat_message.type
    if bots.get(uid) is None:
        bots[uid] = ChatBot(uid)
        await bots[uid].initialize()

    # response = bot.run(chat_message.message, chat_message.img)
    return StreamingResponse(
        bots[uid].chat(thread_id, chat_message.message, chat_message.img, file_type),
        # test_chat(chat_message.message),
        headers=headers
    )
    
    
@app.post("/summarize")
async def summarize(request: Summarize):
    uid = request.uid
    thread_id = request.thread_id
    if bots.get(uid) is None:
        bots[uid] = ChatBot(uid)
        await bots[uid].initialize()
    pdf = await sumarize_history(bots[uid], thread_id)
    def iterfile():
        yield pdf
    # Create a StreamingResponse, which is more memory-efficient
    response = StreamingResponse(iterfile(), media_type="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    return response
    
    
@app.post("/feedback")
async def feedback(request: Feedback):
    thread_id = request.thread_id
    uid = request.uid
    uemail = request.email
    username = request.displayName
    if bots.get(uid) is None:
        bots[uid] = ChatBot(uid)
        await bots[uid].initialize()
    await send_mail(request.feedback, request.rate,  uemail, username, bots[uid].histories[thread_id][1:])
    return {"message": "done"}


@app.post("/contact")
async def contact(request: Contact):
    await send_contact(request.message, request.email, request.name)
    return {"message": "done"}


@app.post("/resetemail")
async def Reset(request: Email):
    await send_ResetEmail(request.message, request.email)
    return {"message": "done"}
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)