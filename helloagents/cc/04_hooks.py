"""Agent hooks: 在固定生命周期插入权限、日志和输出处理。"""

import json
import re

from myagent import Agent, LLM
from myagent.core.hooks import HookContext, HookEvent, Hooks
from myagent.tools.filesystem import edit_file_tool, glob_tool, read_file_tool, write_file_tool
from myagent.tools.shell import bash_tool


def print_user_prompt(context: HookContext) -> None:
    print(f"[hook:prompt] {context.query[:60]}")


def print_agent_info(context: HookContext) -> None:
    print(f"[hook:agent] {context.agent}")


def check_permission(context: HookContext) -> str | None:
    if context.tool.name != "bash":
        return None
    command = context.arguments.get("command", "")
    if re.search(r"(?i)(rm -rf /|sudo|shutdown|reboot|mkfs|dd if=)", command):
        return "Permission denied by deny list"
    if re.search(r"(?i)(^|[;&|()\n])\s*rm\s", command):
        answer = input(f"Allow destructive command {command!r}? [y/N] ")
        if answer.strip().lower() not in {"y", "yes"}:
            return "Permission denied by user"
    return None


def print_tool_result(context: HookContext) -> None:
    """工具结果的显示逻辑放在 hook 中，Agent 本身不关心终端样式。"""
    args = json.dumps(context.arguments, ensure_ascii=False)[:100]
    output = " / ".join(context.result.splitlines()[:2])[:160] or "(no output)"
    print(f"[tool] {context.tool_name}({args}) -> {output}")


def log_session_end(context: HookContext) -> None:
    count = sum(message.get("role") == "tool" for message in context.agent.messages)
    print(f"[hook:stop] tool calls: {count}")


hooks = Hooks()
hooks.on(HookEvent.USER_PROMPT_SUBMIT, print_user_prompt, print_agent_info)
hooks.on(HookEvent.PRE_TOOL_USE, check_permission)
hooks.on(HookEvent.POST_TOOL_USE, print_tool_result)
hooks.on(HookEvent.STOP, log_session_end)

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
