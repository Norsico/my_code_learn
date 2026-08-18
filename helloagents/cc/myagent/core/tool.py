"""
Tool：将一个 Python 函数包装为模型可调用的工具。

- schema()：生成 Function Calling schema
- run()：用模型给出的参数执行实际函数
"""

from collections.abc import Callable
from typing import Any


class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable[..., str],
        parameters: dict[str, dict[str, str]],
        required: list[str] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.function = function
        self.parameters = parameters
        self.required = required or list(parameters)

    def schema(self) -> dict[str, Any]:
        # 转换为模型能识别的 Function Calling 格式。
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": self.required,
                },
            },
        }

    def run(self, arguments: dict[str, Any]) -> str:
        # 将模型给出的参数解包后交给实际函数。
        return str(self.function(**arguments))
