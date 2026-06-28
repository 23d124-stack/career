from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# Load API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(data: ChatRequest):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": data.message
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }
