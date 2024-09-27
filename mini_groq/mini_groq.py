import os
import groq
from groq import Groq
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    timeout=20.0,
    max_retries=1,
)

class Prompt(BaseModel):
    prompt: str

@app.get("/status")
async def get_status():
    return {"message": "OK"}

@app.post("/chat")
async def post_chat(prompt: Prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt.prompt},
            ],
            model="mixtral-8x7b-32768",
        )
        return {"response": chat_completion.choices[0].message.content}

    except groq.APIConnectionError as e:
        raise HTTPException(status_code=500, detail="API Connection Error")

    except groq.RateLimitError as e:
        raise HTTPException(status_code=429, detail="Rate Limit Exceeded")

    except groq.APIStatusError as e:
        raise HTTPException(status_code=e.status_code, detail="API Status Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
