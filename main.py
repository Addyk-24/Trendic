from typing import Union
import uuid
from fastapi import APIRouter

from fastapi import FastAPI
# from app import router


from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from multi_tool_agent.agent import root_agent
from app.schema import UserRequest, AgentResponse


router = APIRouter()

session_service = InMemorySessionService()


@router.get("/")
def root():
    return {
        "message": "Welcome to Trendic",
        "status Code": "200k"
    }
@router.post("/trends")
async def get_trends(payload: UserRequest):

    session_id = str(uuid.uuid4())

    session = await session_service.create_session(
        app_name="trendic_api",
        user_id="api_user",
        session_id=session_id,
    )

    runner = Runner(
        agent=root_agent,
        app_name="trendic_api",
        session_service=session_service,
    )

    result = await runner.run(
        session_id=session.id,
        input=payload.query,
    )

    return AgentResponse(response=result)
    


app = FastAPI(title="Trendic AI")

app.include_router(router)