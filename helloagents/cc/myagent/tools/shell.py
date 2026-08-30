import subprocess

from ..core.tool import Tool
from .workspace import WORKDIR


def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(item in command for item in dangerous):
        return "Error: Dangerous command blocked"
    try:
        result = subprocess.run(command, shell=True, cwd=WORKDIR,
                                capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=120)
        output = (result.stdout + result.stderr).strip()
        return output[:50000] if output else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    except OSError as error:
        return f"Error: {error}"


bash_tool = Tool(
    name="bash",
    description="Run a shell command.",
    function=run_bash,
    parameters={
        "command": {
            "type": "string",
            "description": "要执行的 shell 命令",
        },
    },
)
