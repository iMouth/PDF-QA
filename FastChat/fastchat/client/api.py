from typing import Dict, List, Optional, Union,Iterator,AsyncGenerator
import asyncio
import os
import json
import httpx
from fastapi.responses import StreamingResponse
from fastchat.protocol.chat_completion import (
    ChatCompletionRequest,
    ChatCompletionResponse,
)

_BASE_URL = "http://localhost:8000"

if os.environ.get("FASTCHAT_BASE_URL"):
    _BASE_URL = os.environ.get("FASTCHAT_BASE_URL")


def set_baseurl(base_url: str):
    global _BASE_URL
    _BASE_URL = base_url


class ChatCompletionClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def request_completion(
        self, request: ChatCompletionRequest, timeout: Optional[float] = None
    ) -> Union[ChatCompletionResponse, AsyncGenerator[str, None]]:
        async with httpx.AsyncClient() as client:
            if request.stream:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=request.dict(),
                    timeout=timeout,
                )

                async def content_stream():
                    async for chunk in response.aiter_raw():
                        if chunk:
                            data = json.loads(chunk.decode())
                            if data["error_code"] == 0:
                                output = data["text"]
                                yield output
                            else:
                                output = data["text"] + f" (error_code: {data['error_code']})"
                                yield output
                                return

                return content_stream()
            else:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=request.dict(),
                    timeout=timeout,
                )
                response.raise_for_status()
                return ChatCompletionResponse.parse_obj(response.json())


class ChatCompletion:
    OBJECT_NAME = "chat.completions"

    @classmethod
    def create(cls, *args, **kwargs) -> Union[ChatCompletionResponse, AsyncGenerator[str,None]]:
        """Creates a new chat completion for the provided messages and parameters.
        See `acreate` for more details.
        """
        return asyncio.run(cls.acreate(*args, **kwargs))

    @classmethod
    async def acreate(
        cls,
        model: str,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = 0.7,
        n: int = 1,
        max_tokens: Optional[int] = None,
        stop: Optional[str] = None,
        timeout: Optional[float] = None,
        stream: Optional[bool] = False,
    ) -> Union[ChatCompletionResponse, AsyncGenerator[str,None]]:
        """Creates a new chat completion for the provided messages and parameters."""
        request = ChatCompletionRequest(
            model=model,
            messages=messages,
            temperature=temperature,
            n=n,
            max_tokens=max_tokens,
            stop=stop,
            stream=stream,
        )
        client = ChatCompletionClient(_BASE_URL)
        response = await client.request_completion(request, timeout=timeout)
        return response
