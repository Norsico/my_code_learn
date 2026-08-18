from myagent import Agent, LLM, Tool
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import ANSI
import os
import glob as g
import subprocess
from pathlib import Path
WORKDIR = Path.cwd()

# -- From s01 (unchanged) --

def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=WORKDIR,
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"


# -- New in s02: four tools --

def safe_path(p: str) -> Path:
    path = (WORKDIR / p).resolve()
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"Path escapes workspace: {p}")
    return path


def run_read(path: str, limit: int | None = None) -> str:
    try:
        lines = safe_path(path).read_text().splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more lines)"]
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def run_write(path: str, content: str) -> str:
    try:
        file_path = safe_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = safe_path(path)
        text = file_path.read_text()
        if old_text not in text:
            return f"Error: text not found in {path}"
        file_path.write_text(text.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"


def run_glob(pattern: str) -> str:
    try:
        results = []
        search_pattern = pattern if os.path.isabs(pattern) else str(WORKDIR / pattern)

        for match in g.glob(search_pattern, recursive=True):
            path = Path(match).resolve()
            if path.is_relative_to(WORKDIR):
                results.append(str(path.relative_to(WORKDIR)))

        return "\n".join(results) if results else "(no matches)"
    except Exception as e:
        return f"Error: {e}"

bash_tool = Tool(
    name="bash",
    description="Run a shell command.",
    function=run_bash,
    parameters={
        "command": {
            "type": "string",
            "description": "要执行的 shell 命令",
        }
    },
)
read_file_tool = Tool(
    name="read_file",
    description="Read file contents.",
    function=run_read,
    parameters={
        "path": {
            "type": "string",
            "description": "文件路径",
        },
        "limit": {
            "type": "integer",
            "description": "最多读取的行数，可不传",
        },
    },
    required=["path"],
)
write_file_tool = Tool(
    name="write_file",
    description="Write content to a file.",
    function=run_write,
    parameters={
        "path": {
            "type": "string",
            "description": "文件路径",
        },
        "content": {
            "type": "string",
            "description": "要写入的完整内容",
        },
    },
)
edit_file_tool = Tool(
    name="edit_file",
    description="Replace exact text in a file once.",
    function=run_edit,
    parameters={
        "path": {
            "type": "string",
            "description": "文件路径",
        },
        "old_text": {
            "type": "string",
            "description": "要替换的原文本",
        },
        "new_text": {
            "type": "string",
            "description": "替换后的新文本",
        },
    },
)
glob_tool = Tool(
    name="glob",
    description="Find files matching a glob pattern.",
    function=run_glob,
    parameters={
        "pattern": {
            "type": "string",
            "description": "文件匹配模式，例如 **/*.py",
        },
    },
)


# 入口只负责组装 Agent，不处理工具调用细节。
agent = Agent(
    llm=LLM(provider="alibaba"),
    system_prompt="你是小A，会优雅使用命令行工具。回复不能长篇大论，像人类一样回复就行，不需要emoji，可以使用markdown回复。但注意回复内容非不要不要太长。简洁优雅为主。",
    tools=[bash_tool, read_file_tool, write_file_tool, edit_file_tool, glob_tool],
)

while True:
    try:
        # prompt_toolkit 负责终端编辑和中文宽字符显示。
        query = prompt(
            ANSI("\x1b[36ms01 >> \x1b[0m")
        )
    except (EOFError, KeyboardInterrupt):
        break
    print(agent.run(query))
