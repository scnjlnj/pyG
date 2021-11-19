from collections import deque, defaultdict


class Solution:
    def secondMinimum(self, n: int, edges, time: int, change: int) -> int:
        # 全搜索超时
        edge_map = {x: set() for x in range(1, n + 1)}
        for st, en in edges:
            edge_map[st].add(en)
            edge_map[en].add(st)
        step_set = {1}
        node_fast_map = {1: 1}
        stack = deque([[1]])
        while stack:
            now = stack.popleft()
            cur_node = now[-1]
            node_fast_map[cur_node] = len(now)
            if cur_node == n:
                minsteps = now
            choices = edge_map[cur_node] - step_set
            stack.extend([now + [c] for c in choices])
            step_set = step_set | edge_map[cur_node]
        secmin = len(minsteps) + 2
        # find if delta == 1
        temp = defaultdict(list)
        for node in node_fast_map:
            temp[node_fast_map[node]].append(node)
        print(node_fast_map)
        print(minsteps)
        for ind in range(len(minsteps) - 1):
            ss = set()
            st = minsteps[ind]
            for node in temp[ind + 1]:
                ss |= edge_map[node]
            if st in ss:
                secmin = len(minsteps) + 1
                break
        cur_time = time
        for _ in range(secmin - 2):
            flag = (cur_time // change) % 2  # flag=0 为绿
            rest_time = change - (cur_time % change)
            if flag == 0:
                cur_time += time
            else:
                cur_time += time + rest_time

        return cur_time

print(Solution().secondMinimum(6,[[1,2],[1,3],[2,4],[3,5],[5,4],[4,6]],3,100))