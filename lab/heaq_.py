import heapq
from itertools import count
from math import ceil


class Node():
    def __init__(self,v,cnt=None):
        self.v=v
        self.cnt=1 if not cnt else cnt
    def __lt__(self, other):
        return self.v/self.cnt > other.v/other.cnt
class Solution:
    def minimizedMaximum(self, n: int, quantities) -> int:
        if len(quantities)==n:return max(quantities)
        heaq=[]
        for num in quantities:
            heapq.heappush(heaq,Node(num,1))
        for i in range(len(quantities),n):
            node = heapq.heappop(heaq)
            node.cnt+=1
            heapq.heappush(heaq,node)
        node = heapq.heappop(heaq)
        return ceil(node.v/node.cnt)


print(Node(10)>Node(5))