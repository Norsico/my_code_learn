import glob as glob_module
import os

from ..core.tool import Tool
from .workspace import WORKDIR, safe_path


def run_read_file(path: str, limit: int | None = None) -> str:
    try:
        lines = safe_path(path).read_text(encoding="utf-8").splitlines()
        if limit is not None and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more lines)"]
        return "\n".join(lines)
    except (OSError, ValueError) as error:
        return f"Error: {error}"


def run_write_file(path: str, content: str) -> str:
    try:
        file_path = safe_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} bytes to {path}"
    except (OSError, ValueError) as error:
        return f"Error: {error}"


def run_edit_file(path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = safe_path(path)
        text = file_path.read_text(encoding="utf-8")
        if old_text not in text:
            return f"Error: text not found in {path}"
        file_path.write_text(text.replace(old_text, new_text, 1), encoding="utf-8")
        return f"Edited {path}"
    except (OSError, ValueError) as error:
        return f"Error: {error}"


def run_glob(pattern: str) -> str:
    try:
        search_pattern = pattern if os.path.isabs(pattern) else str(WORKDIR / pattern)
        matches = []
        for match in glob_module.glob(search_pattern, recursive=True):
            path = match if os.path.isabs(match) else str(WORKDIR / match)
            resolved = safe_path(os.path.relpath(path, WORKDIR))
            matches.append(str(resolved.relative_to(WORKDIR)))
        return "\n".join(matches) if matches else "(no matches)"
    except (OSError, ValueError) as error:
        return f"Error: {error}"


read_file_tool = Tool(
    name="read_file",
    description="Read file contents.",
    function=run_read_file,
    parameters={
        "path": {"type": "string", "description": "文件路径"},
        "limit": {"type": "integer", "description": "最多读取的行数，可不传"},
    },
    required=["path"],
)
write_file_tool = Tool(
    name="write_file",
    description="Write content to a file.",
    function=run_write_file,
    parameters={
        "path": {"type": "string", "description": "文件路径"},
        "content": {"type": "string", "description": "要写入的完整内容"},
    },
)
edit_file_tool = Tool(
    name="edit_file",
    description="Replace exact text in a file once.",
    function=run_edit_file,
    parameters={
        "path": {"type": "string", "description": "文件路径"},
        "old_text": {"type": "string", "description": "要替换的原文本"},
        "new_text": {"type": "string", "description": "替换后的新文本"},
    },
)
glob_tool = Tool(
    name="glob",
    description="Find files matching a glob pattern.",
    function=run_glob,
    parameters={
        "pattern": {"type": "string", "description": "文件匹配模式，例如 **/*.py"},
    },
)
