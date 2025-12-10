from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from localagent.types import OpenAiClientConfig

from src.agent.agent import agent_stream_response
from src.settings import settings

app = FastAPI()

client_config = OpenAiClientConfig(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
    llm_model_name=settings.openai_model,
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/agent")
async def agent_response(user_message: str):
    async def stream_response():
        async for response in agent_stream_response(client_config, user_message):
            yield response

    return StreamingResponse(stream_response(), media_type="application/x-ndjson")
