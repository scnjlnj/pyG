class Solution:
    def smallestSubsequence(self, s: str, k: int, letter: str, repetition: int) -> str:

        # 超时了
        # return self.rec(s,k,letter,repetition,s.count(letter))

        stack = []
        l_count = s.count(letter)
        r_count = 0
        for ii,c in enumerate(s):
            flag = 1 if letter==c else 0
            if not stack or (stack[-1] <= c and len(stack)<k):
                if flag: r_count += 1
                stack.append(c)
            elif flag and len(stack)==k and r_count + l_count == repetition and r_count<repetition:
                for ind, x in enumerate(stack[::-1]):
                    if x != c:
                        stack[-1 - ind] = letter
                        r_count+=1
                        break
            elif stack[-1] > c:
                while stack and stack[-1] > c and len(s)-ii >= k-len(stack)+1:
                    if stack[-1]==letter and r_count + l_count > repetition:
                        r_count -= 1
                        stack.pop()
                    elif stack[-1]==letter and r_count + l_count == repetition:
                        break
                    else:
                        stack.pop()
                if len(stack)<k:
                    stack.append(c)
                    if flag: r_count += 1
            if flag: l_count -= 1
        return "".join(stack)
#
print(Solution().smallestSubsequence("wuynymkihfdcbabefiiymnoyyytywzy",
16,
"y",
4))
print(Solution().smallestSubsequence("bezzzzzszvvwxxxz",
7,
"z",
5))
print(Solution().smallestSubsequence("mmmxmxymmm",
8,
"m",
4))
print(Solution().smallestSubsequence("aaabbbcccddd",
3,
"b",
2))
print(Solution().smallestSubsequence("leetcode",
4,
"e",
2))
print(Solution().smallestSubsequence("leet",
3,
"e",
1))
print(Solution().smallestSubsequence("eeeexeeeyexyyeyxeyexyxeyexeexyexxxxyxeye",
7,
"e",
2))
print(Solution().smallestSubsequence("cdjjmnqqrrvwwwxyydvrqqqnhged",
21,
"d",
2))
