"""Hooks 示例：把权限、日志等横向逻辑从 Agent 主循环中移出。"""

import re
import json

from myagent import Agent, LLM
from myagent.core.hooks import (
    POST_TOOL_USE,
    PRE_TOOL_USE,
    STOP,
    USER_PROMPT_SUBMIT,
    PostToolUseContext,
    PreToolUseContext,
    StopContext,
    UserPromptContext,
)
from myagent.tools.filesystem import edit_file_tool, glob_tool, read_file_tool, write_file_tool
from myagent.tools.shell import bash_tool


def log_prompt(context: UserPromptContext) -> None:
    print(f"[hook] user prompt: {context.query[:60]}")


def log_tool(context: PreToolUseContext) -> None:
    print(f"[hook] before {context.tool.name}: {context.arguments}")


def print_tool_result(context: PostToolUseContext) -> None:
    """替代 Agent 内置的 _print_tool_call。显示逻辑属于应用层。"""
    arguments_text = json.dumps(context.arguments, ensure_ascii=False)
    result_text = " / ".join(context.result.splitlines()[:2]) or "(no output)"
    if len(arguments_text) > 100:
        arguments_text = arguments_text[:97] + "..."
    if len(result_text) > 160:
        result_text = result_text[:157] + "..."
    print(f"\033[2;37m[tool] {context.tool_name}({arguments_text}) -> {result_text}\033[0m")


def warn_large_output(context: PostToolUseContext) -> None:
    if len(context.result) > 100_000:
        print(f"[hook] large output from {context.tool_name}: {len(context.result)} chars")


def permission_check(context: PreToolUseContext) -> str | None:
    if context.tool.name != "bash":
        return None
    command = context.arguments.get("command", "")
    if re.search(r"(?i)(rm -rf /|sudo|shutdown|reboot|mkfs|dd if=)", command):
        return "Permission denied by deny list"
    if re.search(r"(?i)(^|[;&|()\n])\s*rm\s", command):
        choice = input(f"Allow destructive command {command!r}? [y/N] ")
        if choice.strip().lower() not in {"y", "yes"}:
            return "Permission denied by user"
    return None


def session_summary(context: StopContext) -> None:
    tool_messages = sum(1 for message in context.agent.messages if message.get("role") == "tool")
    print(f"[hook] session finished, tool calls: {tool_messages}")


hooks = {
    USER_PROMPT_SUBMIT: [log_prompt],
    PRE_TOOL_USE: [permission_check, log_tool],
    POST_TOOL_USE: [print_tool_result, warn_large_output],
    STOP: [session_summary],
}

agent = Agent(
    llm=LLM(provider="alibaba"),
    system_prompt="你是一个简洁的 coding agent。",
    tools=[bash_tool, read_file_tool, write_file_tool, edit_file_tool, glob_tool],
    hooks=hooks,
)


if __name__ == "__main__":
    while True:
        try:
            query = input("s04 >> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if query.lower() in {"q", "exit", ""}:
            break
        print(agent.run(query))
