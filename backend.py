from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import firebase_admin
from firebase_admin import auth

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from coffee_agent.agent import root_agent
from coffee_agent.firebase_service import save_chat


if not firebase_admin._apps:
    firebase_admin.initialize_app()


app = FastAPI(title="Smart Coffee AI Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


APP_NAME = "smart_coffee_ai"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Smart Coffee AI Backend is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(
    request: ChatRequest,
    authorization: str = Header(None),
):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    id_token = authorization.split("Bearer ")[1]

    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    session_id = f"session_{user_id}"

    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
    except Exception:
        pass

    content = types.Content(
        role="user",
        parts=[
            types.Part(text=request.message)
        ],
    )

    final_response = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    save_chat(
        user_id=user_id,
        user_message=request.message,
        assistant_message=final_response,
    )

    return {
        "reply": final_response
    }
