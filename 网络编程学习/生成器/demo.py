from typing import List, Iterator
import math
# print(int(2.8))
# import math


# print(math.ceil())

with open('/Users/xiao/Workspace/Study/helloagents/网络编程学习/生成器/article.txt', "r+") as f:
    # print(f.readlines())
    lines = [line.strip() for line in f.readlines() if line!='\n']
    # print(lines[:10])

# print(lines[:10])

batch_size = 3

def data_loader(batch_size: int, data: List) -> list:
    data_row = len(data)
    batch = int(data_row / batch_size)+1
    null_row = batch_size - int((data_row / batch_size-int(data_row / batch_size))*batch_size) # 寻找缺失行数量
    batched_data = []

    for i in range(batch):
        batched_data.append(data[i*batch_size:(i+1)*batch_size])
        
        # print((i+1)*batch_size)
    for _ in range(null_row):
        batched_data[-1].append('null')
    print(batched_data)
    # print(batched_data)


data_loader(batch_size, lines) # 写的有问题
print("@"*23)

# 自优化后的 yield 生成器版
def my_data_loader(batch_size: int, data: List):
    data_row = len(data)
    # batch = int(data_row / batch_size)+1 # 错误写法
    batch = math.ceil(data_row/batch_size)
    # null_row = batch_size - int((data_row / batch_size-int(data_row / batch_size))*batch_size) # 寻找缺失行数量 (错误写法)

    null_row = batch*batch_size-data_row
    print(type(null_row))
    print(null_row)
    for i in range(batch):
        batched_data= data[i*batch_size:(i+1)*batch_size]
        if i == batch-1:
            for _ in range(null_row):
                batched_data.append('null')
        yield batched_data
        

    # for _ in range(null_row):
    #     batched_data[-1].append('null')
    # print(batched_data)


for batch in my_data_loader(batch_size, lines):
    print(batch)


print("@"*23)

# yield 生成器版

def data_loader_yield(batch_size: int, data: List) -> Iterator[List]:
    # 按 batch_size 步长切分数据
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        # 末批不足 batch_size 时以 'null' 补齐，保持批次大小一致
        while len(batch) < batch_size:
            batch.append('null')
        yield batch


for batch in data_loader_yield(batch_size, lines):
    print(batch)
