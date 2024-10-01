from typing import List, Tuple
from pydantic import BaseModel

# Pydantic model for the chat history input
class ChatHistory(BaseModel):
    history: List[Tuple[str, str]]
    
class ChatMessage(BaseModel):
    message: str
    img:str
    uid: str
    thread_id: str
    type: str

class Feedback(BaseModel):
    uid: str
    email: str
    displayName: str
    feedback: str
    thread_id: str
    rate: int

class Contact(BaseModel):
    name: str
    email: str
    message: str

class Email(BaseModel):
    email: str
    message: str


class Summarize(BaseModel):
    uid: str
    thread_id: str