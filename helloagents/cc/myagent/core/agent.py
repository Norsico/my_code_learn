"""
Agent：维护对话历史，驱动模型与工具的循环。

- add_message()：写入 user、assistant 或 tool 消息
- run()：调用模型、执行工具、回传结果并返回最终回答
- hooks：在 Agent 生命周期节点插入日志、权限等应用逻辑
"""

import json
from typing import Any

from .llm import LLM
from .tool import Tool
from .hooks import HookContext, HookEvent, Hooks


class Agent:
    def __init__(
        self,
        llm: LLM,
        system_prompt: str,
        tools: list[Tool] | None = None,
        max_steps: int | None = None,
        hooks: Hooks | None = None,
    ) -> None:
        self.llm = llm
        # 工具名用于匹配模型返回的 tool_call。
        self.tools = {tool.name: tool for tool in tools or []}
        self.max_steps = max_steps
        self.hooks = hooks or Hooks()
        self.messages = []
        self.add_message("system", system_prompt)

    def __str__(self) -> str:
        return f"Agent(tools={list(self.tools)}, messages={len(self.messages)})"

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

    def run(self, query: str) -> str:
        self.hooks.emit(HookEvent.USER_PROMPT_SUBMIT, HookContext(self, query=query))
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
                self.hooks.emit(HookEvent.STOP, HookContext(self))
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
                        blocked = self.hooks.emit(
                            HookEvent.PRE_TOOL_USE,
                            HookContext(self, tool=tool, arguments=arguments),
                            stop_on_result=True,
                        )
                        if blocked:
                            result = str(blocked)
                        else:
                            try:
                                result = tool.run(arguments)
                            except Exception as error:
                                result = (
                                    f"Tool execution error for '{tool_name}': "
                                    f"{type(error).__name__}: {error}"
                                )
                # 工具成功、失败或被拒绝后都触发同一个事件。
                self.hooks.emit(
                    HookEvent.POST_TOOL_USE,
                    HookContext(self, tool_name=tool_name, arguments=arguments, result=result),
                )
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
        self.hooks.emit(HookEvent.STOP, HookContext(self))
        return message.content or ""
