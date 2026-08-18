from hello_agents import HelloAgentsLLM
import os
import dotenv

dotenv.load_dotenv()

class MyLLM(HelloAgentsLLM):
    def __init__(
            self,
            model = None, 
            api_key = None, 
            base_url = None, 
            provider = None, 
            **kwargs
    ):
        if provider == "DS":
            # self.timeout = 60
            # self.temperature = temperature
            # self.max_tokens = 4096
            super().__init__(
                model=model or os.getenv("DS_MODEL_ID"),
                api_key=api_key or os.getenv("DS_API_KEY"),
                base_url=base_url or os.getenv("DS_BASE_URL"),
            )
        elif provider == 'SiliconFlow':
            super().__init__(
                model=model or os.getenv("SiliconFlow_MODEL_ID"),
                api_key=api_key or os.getenv("SiliconFlow_API_KEY"),
                base_url=base_url or os.getenv("SiliconFlow_BASE_URL"),
            )
        elif provider == 'GPT':
            super().__init__(
                model=model or os.getenv("GPT_MODEL_ID"),
                api_key=api_key or os.getenv("GPT_API_KEY"),
                base_url=base_url or os.getenv("GPT_BASE_URL"),
            )
        else:
            super.__init__()


if __name__ == '__main__':
    my_llm = MyLLM(
        provider='GPT'
    )
    messages = [
        {
            "role": "user",
            "content": "你是什么模型？知识库截止到什么时候"
        }
    ]
    # 迭代器
    # response_stream = my_llm.think(messages=messages)
    # for chunk in response_stream:
    #     pass
    # 或者
    for chunk in my_llm.stream_invoke(messages=messages):
        print(chunk, end='',flush=True)

    # # invoke
    # print(my_llm.invoke(messages=messages))
