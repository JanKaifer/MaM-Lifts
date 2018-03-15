class Everything:
    def __init__(self, state):
        self.house = tuple((tuple((pep for pep in floor)) for floor in state.house))
        self.pos = tuple((tuple((pos[0], pos[1])) for pos in state.pos))
        self.passengers = tuple((tuple((pep for pep in lift)) for lift in state.passengers))
        self.n = state.n
        self.door_time = state.door_time
        self.capacity = state.capacity
        self.get_list = lambda: state.get_list()
        self.vytah = state.vytah


class Lift:
    reducer = Everything
    
    def __call__(self, state):
        from random import choice
        return [choice(["up", "down", "wait", "open"])]
    
    
class RandomLift(Lift):
    to=-1
    
    def __call__(self, state):
        if state.pos[0][1]:
            return ["wait"]
        if state.passengers[0]:
            if state.passengers[0][0].where() == state.pos[0][0]:
                return ["open"]
            elif state.passengers[0][0].where() < state.pos[0][0]:
                return ["down"]
            elif state.passengers[0][0].where() > state.pos[0][0]:
                return ["up"]
            
        if self.to<0:
            from random import choice
            if not state.get_list():
                return ["wait"]
            self.to = choice(state.get_list())[1]
        if self.to == state.pos[0][0]:
            self.to = -1
            return ["open"]
        elif self.to < state.pos[0][0]:
            return ["down"]
        elif self.to > state.pos[0][0]:
            return ["up"]
       
        
class BasicLift(Lift):
    def __call__(self, state):
        if state.pos[0][1]:
            return ["wait"]
        if state.passengers[0]:
            closest = state.passengers[0][0].where()
            for pep in state.passengers[0]:
                if abs(pep.where() - state.pos[0][0]) < abs(closest - state.pos[0][0]):
                    closest = pep.where()
        else:
            closest = -1
            for i in range(state.n):
                if state.house[i] and (closest < 0 or abs(i - state.pos[0][0]) < abs(closest - state.pos[0][0])):
                    closest = i
            if closest < 0:
                return ["wait"]
        if closest == state.pos[0][0]:
            return ["open"]
        elif closest < state.pos[0][0]:
            return ["down"]
        elif closest > state.pos[0][0]:
            return ["up"]
        
        
class MinDistLift(Lift):
    def __call__(self, state):
        if state.pos[0][1]:
            return ["wait"]
        if state.passengers[0]:
            closest = state.passengers[0][0].where()
            for pep in state.passengers[0]:
                if abs(pep.where() - state.pos[0][0]) < abs(closest - state.pos[0][0]):
                    closest = pep.where()
        else:
            closest = -1
            closest_pep = None
            for i in range(state.n):
                for pep in state.house[i]:
                    if closest_pep is None or abs(i - state.pos[0][0])+abs(i - pep.where()) < abs(closest - state.pos[0][0]) + abs(closest_pep.where() - closest):
                        closest = i
                        closest_pep = pep
            if closest_pep is None:
                return ["wait"]
        if closest == state.pos[0][0]:
            return ["open"]
        elif closest < state.pos[0][0]:
            return ["down"]
        elif closest > state.pos[0][0]:
            return ["up"]


class MinDistCollect(Lift):
    def __call__(self, state):
        if state.pos[0][1]:
            return ["wait"]
        if state.passengers[0]:
            closest = state.passengers[0][0].where()
            for pep in state.passengers[0]:
                if abs(pep.where() - state.pos[0][0]) < abs(closest - state.pos[0][0]):
                    closest = pep.where()
        else:
            closest = -1
            closest_pep = None
            for i in range(state.n):
                for pep in state.house[i]:
                    if closest_pep is None or abs(i - state.pos[0][0])+abs(i - pep.where()) < abs(closest - state.pos[0][0]) + abs(closest_pep.where() - closest):
                        closest = i
                        closest_pep = pep
            if closest_pep is None:
                return ["wait"]
        if len(state.passengers[0]) < state.capacity:
            for pep, floor in state.get_list():
                if (floor == state.pos[0][0] and pep.where() < state.pos[0][0] and closest < state.pos[0][0]) or (floor == state.pos[0][0] and pep.where() > state.pos[0][0] and closest > state.pos[0][0]):
                    return ["open"]
        
        if closest == state.pos[0][0]:
            return ["open"]
        elif closest < state.pos[0][0]:
            return ["down"]
        elif closest > state.pos[0][0]:
            return ["up"]

