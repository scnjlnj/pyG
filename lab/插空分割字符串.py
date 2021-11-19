def split_num(num):
    if len(num) == 1:
        return [[int(num)]]
    else:
        block = len(num) - 1
        ret = []
        for i in range(1 << block):
            s = ""
            for j in range(block):
                s += num[j]
                s += "," if i >> (block-1 - j) & 1 else ""
            s += num[-1]
            ret.append(s.split(","))
        return [int(x) for x in ret]

print(split_num("1234"))