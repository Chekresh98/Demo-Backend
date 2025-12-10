import logging
from typing import Literal

from localagent import BaseToolModel, DefaultEnvironment, History, LocalAgent
from localagent.types import Message, OpenAiClientConfig
from pydantic import BaseModel

from src.agent.prompt import render_prompt

# from src.database.session import collection, get_session_by_id

logger = logging.getLogger(__name__)


class EndConversationTool(BaseToolModel, terminating=True):
    end_conversation: Literal[True] = True


class Environment(DefaultEnvironment):
    def __init__(self, history: list[Message], user_message: str):
        history = History.model_validate(
            history + [Message(role="user", content=user_message)]
        )
        rendered_prompt = render_prompt(user_message=user_message)
        super().__init__(
            tools=[EndConversationTool.convert_to_tool()],
            history=history,
            extra_instructions=rendered_prompt,
        )


class AgentResponse(BaseModel):
    type: Literal["text"]
    text: str


async def agent_stream_response(client_config: OpenAiClientConfig, user_message: str):
    # session = get_session_by_id(session_id)
    # if session is None:
    #     collection.insert_one({"_id": session_id, "history": []})
    #     history = []
    # else:
    #     history = session["history"]

    environment = Environment(history=[], user_message=user_message)
    agent = LocalAgent(
        environment=environment,
        openai_client=client_config,
        max_iterations=10,
    )
    try:
        print("Agent started...")
        async for response in agent.stream_text():
            yield response
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # collection.update_one(
        #     {"_id": session_id}, {"$set": {"history": environment.history.model_dump()}}
        # )
        print("\nAgent finished.")
