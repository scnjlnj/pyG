class Solution:
    def countVowelSubstrings(self, word: str) -> int:
        cnt = 0
        if len(word) < 5: return 0
        y = {x: 0 for x in "aeiou"}
        i = 0
        j = 0
        flag = False

        def check(yy):
            for i in yy.values():
                if i <= 0: return False
            return True

        while True:
            if flag and word[j] in y:
                y[word[j]] += 1
                cnt += 1
            elif word[j] in y and not flag:
                y[word[j]] += 1
                if check(y):
                    cnt += 1
                    flag = True
            elif word[j] not in y and flag:
                while y[word[i]] > 1:
                    y[word[i]] -= 1
                    i += 1
                    cnt += 1
                flag = False
                i = j + 1
                y = {x: 0 for x in "aeiou"}
            elif word[j] not in y and not flag:
                i = j + 1
            j += 1
            if i > len(word) - 5 or j == len(word): break
        while i < len(word) and y[word[i]] > 1:
            i += 1
            y[word[i]] -= 1
            cnt += 1
        return cnt


print(Solution().countVowelSubstrings("cuaieuouac"))