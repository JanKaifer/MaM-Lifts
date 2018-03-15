from algoritmy import Lift

intervals = [None] * 10000


class MultiElev(Lift):
    class FoundError(Exception):
        pass
    
    def __call__(self, state):
        
        # state.pos[vytah][{0-patro,1-dvere}]
        # state.passengers[vytah] - seznam lidi
        # state.house[patro] - seznam lidi
        # state.n - pocet pater
        # state.capacity
        # state.get_list()
        
        global intervals
        
        ret = []
        
        if intervals[0] is None:
            delka = state.n // state.vytah
            mod = state.n % state.vytah
            last = 0
            for i in range(state.vytah):
                if (i < mod):
                    intervals[i] = (last, delka + 1)
                    last = last + delka + 1
                else:
                    intervals[i] = (last, delka)
                    last = last + delka
        
        for v in range(state.vytah):
            try:
                if state.pos[0][1]:
                    ret.append("wait")
                    raise self.FoundError
                if len(state.passengers[v]) > 0:
                    if state.passengers[v][0].where() > state.pos[v][0]:
                        ret.append("up")
                        raise self.FoundError
                    if state.passengers[v][0].where() < state.pos[v][0]:
                        ret.append("down")
                        raise self.FoundError
                    else:
                        ret.append("open")
                        raise self.FoundError
                
                min_dist = None
                patro = None
                for i in range(intervals[v][1]):
                    if state.house[intervals[v][0] + i] and (
                            min_dist is None or abs(state.house[intervals[v][0] + i][0].where() - state.pos[v][0]) < min_dist):
                        min_dist = abs(state.house[intervals[v][0] + i][0].where() - state.pos[v][0])
                        patro = i
                if patro is not None:
                    if patro > state.pos[v][0]:
                        ret.append("up")
                        raise self.FoundError
                    if patro < state.pos[v][0]:
                        ret.append("down")
                        raise self.FoundError
                    else:
                        ret.append("open")
                        raise self.FoundError
                else:
                    if state.pos[v][0] >= intervals[v][0] + intervals[v][1]:
                        ret.append("down")
                        raise self.FoundError
                    if state.pos[v][0] < intervals[v][0]:
                        ret.append("up")
                        raise self.FoundError
                    else:
                        ret.append("wait")
                        raise self.FoundError
            except self.FoundError:
                pass
        return ret
