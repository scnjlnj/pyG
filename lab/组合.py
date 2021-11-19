class State():
    def __init__(self, r, c, dir):
        self.r = r
        self.c = c
        self.dir = dir

    @classmethod
    def get_init_choices(cls, r, c, kind):
        if kind == "rook":
            return [
                State(r, c, (0, 1)),
                State(r, c, (0, -1)),
                State(r, c, (1, 0)),
                State(r, c, (-1, 0)),
                State(r, c, (0, 0))
            ]
        elif kind == "queen":
            return [
                State(r, c, (0, 1)),
                State(r, c, (0, -1)),
                State(r, c, (1, 0)),
                State(r, c, (-1, 0)),
                State(r, c, (1, 1)),
                State(r, c, (-1, -1)),
                State(r, c, (1, -1)),
                State(r, c, (-1, 1)),
                State(r, c, (0, 0))
            ]
        else:
            return [
                State(r, c, (1, 1)),
                State(r, c, (-1, -1)),
                State(r, c, (1, -1)),
                State(r, c, (-1, 1)),
                State(r, c, (0, 0))
            ]

    @classmethod
    def get_choices(cls, obj):
        if obj.dir == (0, 0):
            return [State(obj.r, obj.c, (0, 0))]
        else:
            return [State(obj.r, obj.c, (0, 0)), State(obj.r, obj.c, obj.dir)]

    @classmethod
    def is_finish(cls, states):
        for obj in states:
            if obj.dir == (0, 0):
                continue
            else:
                return False
        return True

    def pass_time(self):
        return (self.r + self.dir[0], self.c + self.dir[1])

    def __repr__(self):
        return f"<({self.r},{self.c},dir:{self.dir})>"


class Solution:
    def enum_ll(self, ll):
        if not ll: return [[]]
        ret = []
        for i in ll[-1]:
            ret += [son + [i] for son in self.enum_ll(ll[:-1])]
        return ret

    def enum_list(self, ll):
        print(ll)
        list1 = ll
        code = f"[[{','.join(['p{}'.format(i) for i in range(len(list1))])}] {''.join(['for p{} in list1[{}] '.format(i, i) for i in range(len(list1))])}]"
        return eval(code)

    def check(self, pos):
        pos_set = set()
        for p in pos:
            if p in pos_set: return False
            pos_set.add(p)
            r, c = p
            if (not 1 <= r <= 8) or (not 1 <= c <= 8): return False
        return True

    def countCombinations(self, pieces, positions) -> int:
        cnt = 0
        init_choices = [State.get_init_choices(*positions[i], pieces[i]) for i in range(len(pieces))]
        cur_states = self.enum_ll(init_choices)
        print(cur_states)
        while cur_states:
            next_states = []
            for states in cur_states:
                print(states)
                if State.is_finish(states):
                    cnt += 1
                    continue
                pos = []
                next_choices = []
                for ss in states:
                    print(ss)
                    pos.append(ss.pass_time())
                    next_choices.append(State.get_choices(State(ss.r+ss.dir[0],ss.c+ss.dir[1],ss.dir)))
                if self.check(pos):
                    next_states += self.enum_ll(next_choices)
            cur_states = next_states

        return cnt

print(Solution().countCombinations(["rook","rook"],
[[1,1],[8,8]]))