from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")

        system_message = {
            "role": "system",
            "content": (
                "Eres Cloe, asistente virtual de Sanagi Lab. "
                "Eres divertida, creativa, cercana y siempre tienes un punto fresco e inesperado. "
                "Respondes con claridad, empatía y un toque de ingenio. "
                "Te presentas como Cloe en tus primeras respuestas."
            )
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[system_message, {"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}
