"""
LLM：OpenAI 兼容接口的轻量客户端。

- __init__()：读取供应商配置并创建 OpenAI 客户端
- invoke()：发送一轮消息并返回模型原始 message
"""

import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLM:
    def __init__(self, provider: str) -> None:
        if provider == "alibaba":
            self.base_url = os.getenv("ALIBABA_BASE_URL")
            self.api_key = os.getenv("ALIBABA_API_KEY")
            self.model_id = os.getenv("ALIBABA_MODEL_ID")

        self._client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=60,
        )

    def invoke(
        self,
        messages: list[dict[str, Any]],
        model_id: str | None = None,
        tools: list[Any] | None = None,
        tool_choice: str | None = None,
    ) -> Any:
        # 只组装本次请求，消息历史由 Agent 管理。
        request: dict[str, Any] = {
            "messages": messages,
            "model": model_id or self.model_id,
            "stream": False,
        }
        if tools is not None:
            request["tools"] = [tool.schema() for tool in tools]
        if tool_choice is not None:
            request["tool_choice"] = tool_choice

        response = self._client.chat.completions.create(
            **request,
        )
        return response.choices[0].message