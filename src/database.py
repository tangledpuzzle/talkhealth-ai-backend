from motor.motor_asyncio import AsyncIOMotorClient


client1 = AsyncIOMotorClient("mongodb+srv://devhunter128:Passw0rdshortsIO@cluster0.foajmas.mongodb.net/")
db = client1['TalkhealthAI']


# Async read operation
async def read_history(user_id):
    try:
        # Select the database    
        histories_collection = db["Chat"]
        cursor = histories_collection.find({"user_id": user_id})
        result = {}
        async for item in cursor:
            item.pop('_id', None)
            key = item['thread']
            if key not in result:
                result[key] = []
            result[key].append(item)
        return result
    except TypeError as e:
        raise ValueError("There was a TypeError in accessing the chat history.") from e
    except Exception as e:
        raise ValueError("An unexpected error occurred.") from e

# Async create operation
async def insert_chat(document):
    collection = db['Chat']
    result = await collection.insert_one(document)
    print(f"Document inserted with id: {result.inserted_id}")

# Async update operation
async def update_document(query, new_values):
    collection = db['example_collection']
    return await collection.update_one(query, {'$set': new_values})

# Async delete operation
async def delete_document(query):
    collection = db['example_collection']
    return await collection.delete_one(query)