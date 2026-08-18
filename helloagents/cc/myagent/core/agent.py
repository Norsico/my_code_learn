"""
Agent：维护对话历史，驱动模型与工具的循环。

- add_message()：写入 user、assistant 或 tool 消息
- run()：调用模型、执行工具、回传结果并返回最终回答
- _print_tool_call()：在终端显示工具调用摘要
"""

import json
from typing import Any

from .llm import LLM
from .tool import Tool


class Agent:
    def __init__(
        self,
        llm: LLM,
        system_prompt: str,
        tools: list[Tool] | None = None,
        max_steps: int | None = None,
    ) -> None:
        self.llm = llm
        # 工具名用于匹配模型返回的 tool_call。
        self.tools = {tool.name: tool for tool in tools or []}
        self.max_steps = max_steps
        self.messages = []
        self.add_message("system", system_prompt)

    def add_message(
        self,
        role: str,
        content: str | None = None,
        tool_calls: list[dict[str, Any]] | None = None,
        tool_call_id: str | None = None,
    ) -> None:
        message: dict[str, Any] = {
            "role": "tool" if tool_call_id else role,
            "content": content,
        }
        if tool_calls is not None:
            message["tool_calls"] = tool_calls
        if tool_call_id is not None:
            message["tool_call_id"] = tool_call_id
        self.messages.append(message)

    def _print_tool_call(
        self,
        name: str,
        arguments: dict[str, Any],
        result: str,
    ) -> None:
        # 终端仅显示工具调用摘要，完整结果仍保留给模型。
        arguments_text = json.dumps(arguments, ensure_ascii=False)
        result_lines = result.splitlines()[:2]
        result_text = " / ".join(result_lines) or "(no output)"
        if len(arguments_text) > 100:
            arguments_text = arguments_text[:97] + "..."
        if len(result_text) > 160:
            result_text = result_text[:157] + "..."
        print(f"\033[2;37m[tool] {name}({arguments_text}) → {result_text}\033[0m")

    def run(self, query: str) -> str:
        self.add_message("user", query)

        steps = 0
        # 默认不限制工具轮数；显式传入 max_steps 时才限制。
        while self.max_steps is None or steps < self.max_steps:
            steps += 1
            message = self.llm.invoke(
                messages=self.messages,
                tools=list(self.tools.values()),
            )
            self.add_message(
                "assistant",
                message.content,
                tool_calls=[tool_call.model_dump() for tool_call in message.tool_calls]
                if message.tool_calls else None,
            )

            if not message.tool_calls:
                return message.content or ""

            # 执行模型请求的工具，并把结果写回对话历史。
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = {}
                try:
                    arguments = json.loads(tool_call.function.arguments)
                    if not isinstance(arguments, dict):
                        raise TypeError("arguments must be a JSON object")
                except (json.JSONDecodeError, TypeError) as error:
                    result = f"Tool argument error for '{tool_name}': {error}"
                else:
                    tool = self.tools.get(tool_name)
                    if tool is None:
                        available_tools = ", ".join(self.tools) or "none"
                        result = (
                            f"Tool not found: '{tool_name}'. "
                            f"Available tools: {available_tools}"
                        )
                    else:
                        try:
                            result = tool.run(arguments)
                        except Exception as error:
                            result = (
                                f"Tool execution error for '{tool_name}': "
                                f"{type(error).__name__}: {error}"
                            )

                self._print_tool_call(tool_name, arguments, result)
                self.add_message(
                    "tool",
                    result,
                    tool_call_id=tool_call.id,
                )

        # 工具额度用尽后，禁止工具调用并要求模型直接作答。
        message = self.llm.invoke(
            messages=self.messages,
            tools=[],
            tool_choice="none",
        )
        self.add_message("assistant", message.content)
        return message.content or ""
