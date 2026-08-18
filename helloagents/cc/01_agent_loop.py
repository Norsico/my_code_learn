from myagent import Agent, LLM, Tool
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import ANSI
import os
import subprocess


def run_bash(command: str) -> str:
    # 阻止明显危险的命令，避免模型直接执行。
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=os.getcwd(),
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"


bash_tool = Tool(
    name="bash",
    description="运行终端命令。仅在用户要求查看或操作本机环境时使用。",
    function=run_bash,
    parameters={
        "command": {
            "type": "string",
            "description": "要执行的 shell 命令",
        }
    },
)

# 入口只负责组装 Agent，不处理工具调用细节。
agent = Agent(
    llm=LLM(provider="alibaba"),
    system_prompt="你是小A，会优雅使用命令行工具。回复不能长篇大论，像人类一样回复就行，不需要emoji，可以使用markdown回复。但注意回复内容非不要不要太长。简洁优雅为主。",
    tools=[bash_tool],
)

# 模型返回结构参考（OpenAI SDK 的 ChatCompletion，附原始字段）：
# 平时调试工具调用时，重点看 choices[0].message：
#   content          —— 最终文本（无工具调用时才有意义）
#   tool_calls       —— 模型请求的工具列表（有值时进入 tool loop）
#   reasoning_content —— 推理模型特有的思考过程，可忽略
#
# ChatCompletion(
#   id='chatcmpl-3d1ce943-9d43-93c9-9d5d-b96e1d4f9ea3',
#   object='chat.completion',
#   created=1787036174,
#   model='deepseek-v4-flash-0731',
#   service_tier=None,
#   system_fingerprint=None,
#   choices=[
#     Choice(
#       finish_reason='stop',
#       index=0,
#       logprobs=None,
#       message=ChatCompletionMessage(
#         role='assistant',
#         content='我是小A，你的智能助手，擅长各种任务的操作与问题解答，包括日常对话、信息查询、工具使用指导等。\n\n如果需要优雅高效地完成某个目标，可以随时告诉我哦！',
#         refusal=None,
#         annotations=None,
#         audio=None,
#         function_call=None,
#         tool_calls=None,          # <- 若不是 None，说明模型要调用工具
#         reasoning_content='哦，用户问我是谁，这是个简单的自我介绍问题。需要简洁明了地说明身份定位，同时突出核心功能特点。可以用轻松友好的语气，强调实用性和服务性。想到要包含几个关键点：名字、功能范围、服务专长。用✨符号增加亲和力，最后可以加个激励性短句收尾。',
#       ),
#     ),
#   ],
#   usage=CompletionUsage(
#     completion_tokens=127,
#     prompt_tokens=95,
#     total_tokens=222,
#     completion_tokens_details=CompletionTokensDetails(
#       accepted_prediction_tokens=None,
#       audio_tokens=None,
#       reasoning_tokens=71,       # <- 推理过程也算 token
#       rejected_prediction_tokens=None,
#     ),
#     prompt_tokens_details=PromptTokensDetails(
#       audio_tokens=None,
#       cached_tokens=0,
#     ),
#   ),
# )

while True:
    try:
        # prompt_toolkit 负责终端编辑和中文宽字符显示。
        query = prompt(
            ANSI("\x1b[36ms01 >> \x1b[0m")
        )
    except (EOFError, KeyboardInterrupt):
        break
    print(agent.run(query))
