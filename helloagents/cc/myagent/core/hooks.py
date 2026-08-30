"""Agent 生命周期 hooks。

所有 hook 都接收同一种 HookContext。未参与当前事件的字段为 None。
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .agent import Agent
    from .tool import Tool


class HookEvent(StrEnum):
    USER_PROMPT_SUBMIT = "user_prompt_submit"
    PRE_TOOL_USE = "pre_tool_use"
    POST_TOOL_USE = "post_tool_use"
    STOP = "stop"


@dataclass
class HookContext:
    agent: Agent
    query: str | None = None
    tool: Tool | None = None
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None
    result: str | None = None


Hook = Callable[[HookContext], Any]


class Hooks:
    """按事件注册多个 hook，并按注册顺序触发。"""

    def __init__(self) -> None:
        self._handlers: dict[HookEvent, list[Hook]] = {
            event: [] for event in HookEvent
        }

    def on(self, event: HookEvent, *handlers: Hook) -> None:
        self._handlers[event].extend(handlers)

    def emit(self, event: HookEvent, context: HookContext, *, stop_on_result: bool = False) -> Any:
        for handler in self._handlers[event]:
            result = handler(context)
            if stop_on_result and result is not None:
                return result
        return None
