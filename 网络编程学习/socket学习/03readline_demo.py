# 先造一个 3 行的小文件来演示
with open('./demo.txt', 'w') as f:
    f.write("第一行\n")
    f.write("第二行\n")
    f.write("第三行\n")

print("========== 1. readline()：每次读一行 ==========")
f = open('./demo.txt', 'r')
print("第1次调用:", repr(f.readline()))   # 读第一行
print("第2次调用:", repr(f.readline()))   # 再调，读第二行
print("第3次调用:", repr(f.readline()))   # 第三行
print("第4次调用:", repr(f.readline()))   # 没了，返回空字符串 ''
f.close()

print("\n========== 2. readlines()：一次读完，返回列表 ==========")
f = open('./demo.txt', 'r')
lines = f.readlines()
print("返回类型:", type(lines))
print("列表内容:", lines)
f.close()

print("\n========== 3. readlines 返回的列表怎么用 ==========")
f = open('./demo.txt', 'r')
for i, line in enumerate(f.readlines(), 1):
    print(f"第{i}行去掉换行: {line.strip()}")
f.close()

print("\n========== 4. 混用的坑：指针会移动 ==========")
f = open('./demo.txt', 'r')
print("先 readline 读一行:", repr(f.readline()))
print("再 readlines():", f.readlines())   # 只剩后面两行
f.close()

print("\n========== 5. for line in f 和 readline 等价 ==========")
with open('./demo.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        print("while 版:", line.strip())

