import json
import re

from dotenv import load_dotenv
from hello_agents import SimpleAgent,Config,HelloAgentsLLM,Message,ToolRegistry,CalculatorTool
from my_llm import MyLLM
from typing import Optional
from hello_agents.tools.base import Tool, ToolResponse
from hello_agents.tools import ToolParameter
# class Agent():
#     def __init__(self,base_url):
#         self.base_url = base_url
    
#     def run(self,name):
#         print(f"{self.base_url}, {name}")

class MySimpleAgent(SimpleAgent):
    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: str | None = None,
            config: Optional[Config] = None,
            enable_tool_calling: bool = True,
            # tool_registry=ToolRegistry
            tool_registry: Optional[ToolRegistry] = None,
    ):
        super().__init__(name,llm,system_prompt,config)
        self.tool_registry = tool_registry
        self.enable_tool_calling = enable_tool_calling and self.tool_registry is not None
    
    def run(self, input_text: str, max_tool_iterations: int = 3, **kwargs) -> str:
        """
        重写的运行方法 - 实现简单对话逻辑，支持可选工具调用
        """
        print(f"🤖 {self.name} 正在处理: {input_text}")

        # 构建消息列表
        messages = []

        # 添加系统消息
        messages.append({"role": "system", "content": self.system_prompt})
        # print(self.system_prompt)

        # 添加历史消息
        for msg in self.history_manager.get_history():
            messages.append({"role": msg.role, "content": msg.content})

        # 添加当前用户消息
        messages.append({"role": "user", "content": input_text})

        if not self.enable_tool_calling:
            response = self.llm.invoke(messages=messages)
            self.add_message(Message(input_text,'user'))
            self.add_message(Message(response.content, 'assistant'))
            print(f"✅ {self.name} 响应完成")
            # print(response)
            return response
        
        tool_schema = self._build_tool_schemas()

        current_iterations = 0
        while current_iterations < max_tool_iterations:
            current_iterations+=1
            print(f"---Current Iterations: {current_iterations}---")
            # self._run_with_tools(messages,input_text,max_tool_iterations)
            response = self.llm.invoke_with_tools(
                messages=messages,
                tools=tool_schema,
            )
            tool_calls = response.tool_calls
            if not response.tool_calls:
                final_answer = response.content or "空 消息"
                self.add_message(Message(input_text,'user'))
                self.add_message(Message(final_answer,'assistant'))
                return response.content
            messages.append({
                'role': 'assistant',
                'content': response.content,
                'tool_calls': [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": tc.arguments
                        }
                    } for tc in response.tool_calls
                ]
            })
            for tool_call in tool_calls:
                tool_call_name = tool_call.name
                tool_call_id = tool_call.id
                
                arguments = json.loads(tool_call.arguments)

                print(f"🎬 调用工具: {tool_call_name}({arguments})")
                result = self._execute_tool_call(tool_call_name, arguments)
                print(f"👀 观察工具调用结果: {result}")

                # 添加工具结果到消息
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": result
                })

        print("⏰ 已达到最大步数，流程终止。")
        final_answer = "抱歉，我无法在限定步数内完成这个任务。"
        
        self.add_message(Message(input_text, 'user'))
        self.add_message(Message(final_answer, 'assistant'))
        return final_answer


    # def stream_run(self, input_text, **kwargs):

    #     messages = []
    #     messages.append({"role":"system","content":self.system_prompt})
    #     for msg in self._history:
    #         messages.append({"role":msg.role,"content":msg.content})
    #     messages.append({"role":"user","content":input_text})
    #     response = ""
    #     print("📝 实时响应: ", end="")
    #     for chunk in self.llm.think(messages,temperature=0.7):
    #         response += chunk
    #         # print(chunk, end="", flush=True)
    #         yield chunk
    #     self.add_message(Message(input_text,'user'))
    #     # print(response)
    #     # print(type(response))
    #     self.add_message(Message(response.content,'assistant'))
    

    # def _run_with_tools(self,messages,input_text,max_tool_iterations):
    #     current_iterations = 0
    #     final_response = ""
    #     while current_iterations < max_tool_iterations:

    #         response = self.llm.invoke(messages=messages)
    #         tool_calls = self._parse_tool_calls(response)
    #         if tool_calls:
    #             print(f"🔧 检测到 {len(tool_calls)} 个工具调用")
    #             tool_results = []
    #             clean_response = response
    #             for call in tool_calls:
    #                 result = self._execute_tool_call(call['tool_name'], call['parameters'])
    #                 tool_results.append(result)
    #                 # 移除调用标记
    #                 clean_response = clean_response.replace(call['original'], "")
                
    #             messages.append({"role": "assistant", "content": clean_response})
    #             tool_results_text = "\n\n".join(tool_results)
    #             messages.append(
    #                 {
    #                     "role": "user", 
    #                     "content": f"工具执行结果:\n{tool_results_text}\n\n请基于这些结果给出完整的回答。"
    #                 }
    #             )
    #             current_iterations += 1
    #             continue
    #         final_response = response
    #         break

    #     if current_iterations>=max_tool_iterations and not final_response:
    #         final_response = self.llm.invoke(messages)

    #     self.add_message(Message(input_text,'user'))
    #     self.add_message(Message(final_response, 'assistant'))
    #     print(f"✅ {self.name} 响应完成")
    #     return final_response

    # def _execute_tool_call(self, tool_name: str, parameters: str) -> str:
    #     """执行工具调用"""
    #     if not self.tool_registry:
    #         return f"❌ 错误:未配置工具注册表"

    #     try:
    #         # 智能参数解析
    #         if tool_name == 'calculator':
    #             # 计算器工具直接传入表达式
    #             print("计算器工具直接传入表达式")
    #             result = self.tool_registry.execute_tool(tool_name, parameters)
    #         else:
    #             # 其他工具使用智能参数解析
    #             param_dict = self._parse_tool_parameters(tool_name, parameters)
    #             tool = self.tool_registry.get_tool(tool_name)
    #             if not tool:
    #                 return f"❌ 错误:未找到工具 '{tool_name}'"
    #             print(f"param_dict: {param_dict}")
    #             result = tool.run(param_dict)

    #         return f"🔧 工具 {tool_name} 执行结果:\n{result}"

    #     except Exception as e:
    #         return f"❌ 工具调用失败:{str(e)}"

    # def _parse_tool_parameters(self, tool_name: str, parameters: str) -> dict:
    #     """智能解析工具参数"""
    #     param_dict = {}

    #     if '=' in parameters:
    #         # 格式: key=value 或 action=search,query=Python
    #         if ',' in parameters:
    #             # 多个参数:action=search,query=Python,limit=3
    #             pairs = parameters.split(',')
    #             for pair in pairs:
    #                 if '=' in pair:
    #                     key, value = pair.split('=', 1)
    #                     param_dict[key.strip()] = value.strip()
    #         else:
    #             # 单个参数:key=value
    #             key, value = parameters.split('=', 1)
    #             param_dict[key.strip()] = value.strip()
    #     else:
    #         # 直接传入参数，根据工具类型智能推断
    #         if tool_name == 'search':
    #             param_dict = {'query': parameters}
    #         elif tool_name == 'memory':
    #             param_dict = {'action': 'search', 'query': parameters}
    #         else:
    #             param_dict = {'input': parameters}

    #     return param_dict

    # def _parse_tool_calls(self,text):
    #     """解析文本中的工具调用"""
    #     pattern = r'\[TOOL_CALL:([^:]+):([^\]]+)\]'
    #     matches = re.findall(pattern, text)

    #     tool_calls = []
        
    #     for tool_name, parameters in matches:
    #         print(f"parameters.strip():{parameters.strip()}")
    #         tool_calls.append({
    #             'tool_name': tool_name.strip(),
    #             'parameters': parameters.strip(),
    #             'original': f'[TOOL_CALL:{tool_name}:{parameters}]'
    #         })

    #     return tool_calls

# def get_weather():
#     return "晴天"

class GetWeather(Tool):
    def __init__(self):
        super().__init__(
            name="get_current_weather",
            description="获取当前位置的天气情况"
        )
    def run(self, parameters) -> ToolResponse:
        param_location = parameters.get("input_location", "none").strip()
        param_day = parameters.get("input_day", "").strip()
        return ToolResponse.success(
            f"到{param_day}的时候，{param_location} 预估为晴天"
        )

    def get_parameters(self):
        return [
            ToolParameter(
                name="input_location",
                type="str",
                description="输入的位置信息，默认为北京"
            ),
            ToolParameter(
                name="input_day",
                type="str",
                description="输入的时间，如周一、周二、周三等。仅能输入两个字"
            )
        ]


if __name__ == '__main__':
     # 加载环境变量
    load_dotenv()

    # 创建LLM实例
    llm = MyLLM(provider='GPT')

    # 注册工具类
    tool_registry = ToolRegistry()

    # 创建工具类
    calculator = CalculatorTool()
    get_weather_tool = GetWeather()

    # 注册工具
    tool_registry.register_tool(calculator)
    tool_registry.register_tool(get_weather_tool)

    my_agnet = MySimpleAgent(
        name='mytoy',
        llm=llm,
        system_prompt="你是一个友好的AI助手，请用简洁明了的方式回答问题。",
        tool_registry=tool_registry
    )
    # print(my_agnet.enable_tool_calling)
    while True:
        try:
            user_input = input("> ")
            print(my_agnet.run(user_input))
            print()
            # for _ in my_agnet.stream_run(user_input):
            #     pass
        except KeyboardInterrupt as e:
            break
             


            





