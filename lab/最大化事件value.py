class Solution:
    def next_choices(self, cur_ind, events):
        if cur_ind == len(events) - 1:
            return []
        if cur_ind == -1:
            s, e, _ = 0, 0, 0
        else:
            s, e, _ = events[cur_ind]
        left_min = float("inf")
        cur_ind += 1
        ret = []
        while cur_ind < len(events):
            ss, ee, vv = events[cur_ind]
            if ss <= e:
                cur_ind += 1
                continue
            if ss > left_min: break
            left_min = min(left_min, ee)
            ret.append(cur_ind)
            cur_ind += 1
        return ret

    def maxTwoEvents(self, events: List[List[int]]) -> int:
        temp = {}
        events = sorted(events, key=lambda x: x[0])
        cur = self.next_choices(-1, events)

        # print(self.next_choices(-1,events))
        # print(self.next_choices(0,events))
        # print(self.next_choices(1,events))
        # return 1
        def func(i):
            if i not in temp:
                choices = self.next_choices(i, events)
                if not choices:
                    temp[i] = events[i][2]
                else:
                    temp[i] = events[i][2] + max([func(ii) for ii in choices])
            return temp[i]

        a = max([func(ii) for ii in cur])
        print(events)
        print(temp)
        return a