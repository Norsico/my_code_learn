from myagent import Agent, LLM
from myagent.tools.filesystem import edit_file_tool, glob_tool, read_file_tool, write_file_tool
from myagent.tools.shell import bash_tool
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import ANSI


agent = Agent(
    llm=LLM(provider="alibaba"),
    system_prompt="你是小A，会优雅使用命令行工具。回复简洁。",
    tools=[bash_tool, read_file_tool, write_file_tool, edit_file_tool, glob_tool],
)

while True:
    try:
        query = prompt(ANSI("\x1b[36ms02 >> \x1b[0m"))
    except (EOFError, KeyboardInterrupt):
        break
    print(agent.run(query))
