from collections import deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # 入度表
        indegree = [0]*numCourses
        # 邻接表
        graph = [[]for _ in range(numCourses)]
        # 队列
        my_deque = deque()
        # 弹出课程数量
        num_course = 0
        # 构造入度表和邻接表
        for now, pre in prerequisites:
            indegree[now] += 1
            graph[pre].append(now)
        # 首次遍历，找到入度表中为0的起始课程
        for start in range(numCourses):
            if indegree[start] == 0:
                my_deque.append(start)
        # 队列弹出，循环处理
        while my_deque:
            left = my_deque.popleft()
            num_course+=1
            for i in graph[left]:
                indegree[i] -= 1
                if indegree[i] == 0:
                    my_deque.append(i)
        return True if num_course == numCourses else False



        

# print([[] for _ in range(3)])
# print([0]*3)
# for i,j in [[1]]:
#     print(i,j)