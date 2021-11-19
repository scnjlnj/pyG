from collections import defaultdict


class Trie:
    left: "Trie" = None
    right: "Trie" = None
    # 由于我们的字典树需要支持删除数的操作
    # 因此这里使用 cnt 变量进行记录该节点对应的数的个数
    cnt: int = 0

class Solution:

    # 最大的数的二进制表示不会超过 18 位
    # 那么二进制位的下标范围为 [0, 17]
    MAXD = 17

    def maxGeneticDifference(self, parents , queries):
        n = len(parents)

        # 将 parents 存储为树的形式，方便进行深度优先遍历
        edges = defaultdict(list)
        # 找出根节点
        root = -1
        for i, parent in enumerate(parents):
            if parent == -1:
                root = i
            else:
                edges[parent].append(i)

        q = len(queries)
        # 使用离线的思想，stored[i] 存储了所有节点 i 对应的询问
        stored = defaultdict(list)
        ans = [0] * q
        for i, (node, val) in enumerate(queries):
            stored[node].append((i, val))

        r = Trie()

        # 向字典树添加一个数
        def trie_insert(x: int) -> None:
            cur = r
            for i in range(Solution.MAXD, -1, -1):
                if x & (1 << i):
                    if not cur.right:
                        cur.right = Trie()
                    cur = cur.right
                else:
                    if not cur.left:
                        cur.left = Trie()
                    cur = cur.left
                cur.cnt += 1

        # 对于给定的 x，返回字典树中包含的数与 x 进行异或运算可以达到的最大值
        def trie_query(x: int) -> int:
            cur, ret = r, 0
            for i in range(Solution.MAXD, -1, -1):
                if x & (1 << i):
                    if cur.left and cur.left.cnt:
                        ret |= (1 << i)
                        cur = cur.left
                    else:
                        cur = cur.right
                else:
                    if cur.right and cur.right.cnt:
                        ret |= (1 << i)
                        cur = cur.right
                    else:
                        cur = cur.left
            return ret

        # 从字典树中删除一个数
        def trie_erase(x: int) -> None:
            cur = r
            for i in range(Solution.MAXD, -1, -1):
                if x & (1 << i):
                    cur = cur.right
                else:
                    cur = cur.left
                cur.cnt -= 1

        # 深度优先遍历
        def dfs(u: int) -> None:
            trie_insert(u)
            for idx, num in stored[u]:
                ans[idx] = trie_query(num)
            for v in edges[u]:
                dfs(v)
            trie_erase(u)

        dfs(root)
        return ans
#
# 作者：LeetCode-Solution
# 链接：https://leetcode-cn.com/problems/maximum-genetic-difference-query/solution/cha-xun-zui-da-ji-yin-chai-by-leetcode-s-sybl/
# 来源：力扣（LeetCode）
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。