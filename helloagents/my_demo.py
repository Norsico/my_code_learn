from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    timeout=60
)

messages = [
    {"role": "system", "content": "You are a helpful assistant that writes Python code."},
    {"role": "user", "content": "仅输出 《静夜思》"}
]
try:
    response = client.chat.completions.create(
        messages=messages,
        model=os.getenv("LLM_MODEL_ID"),
        stream=True,
        temperature=0
    )
    content_start = True
    for chunk in response:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        # content = chunk.choices[0].delta.content
        if delta.reasoning_content:
            print(delta.reasoning_content, end="", flush=True)

        if delta.content:
            if content_start:
                print()
                print("#"*30)
                content_start = False
            print(delta.content, flush=True,end="")
        # print(chunk)
    print()

    # print(response.choices[0].delta)
    # for chunk in response:
    #     if not chunk.choices:
    #         continue
    #     content = chunk[0].delta.content
except Exception as e:
    print(f"{e}")



