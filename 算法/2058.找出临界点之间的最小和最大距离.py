from typing import List,Optional
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:

        last_num = 0
        index = 0
        is_first = True
        res = []
        while head and head.next:
            index += 1
            if is_first:
                last_num = head.val
                is_first = False
                head = head.next
            else:
                # 判断是否为极大值
                if head.val > last_num and head.val > head.next.val:
                    res.append(index)
                elif head.val < last_num and head.val < head.next.val:
                    res.append(index)   
                last_num = head.val
                head = head.next
        # print(res)
        len_res = len(res)
        if not res:
            return [-1,-1]
        if len_res == 1:
            return [-1,-1]
        if len_res == 2:
            return [res[1]-res[0],res[1]-res[0]]
        sub_res = []
        for i in range(1,len_res):
            sub_res.append(res[i]-res[i-1])

        return [min(sub_res), res[-1]-res[0]]



def build_node(list):
    dummy = ListNode()
    cur = dummy
    for i in list:
        cur.next = ListNode(i)
        cur = cur.next
    return dummy.next

if __name__ == '__main__':
    head = [5,3,1,2,5,1,2]
    root = build_node(head)

    s = Solution()
    res = s.nodesBetweenCriticalPoints(root)
    print(res)


