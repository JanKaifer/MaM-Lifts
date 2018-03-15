from random import random, choice


class Person:
    def __init__(self, where=0):
        self._where = where
        self._time = 0
    
    def tick(self, times=1):
        self._time += times
    
    def get_feedback(self):
        return self._time
    
    def where(self):
        return self._where


class Generator:
    def __init__(self, probabilities):
        self.probabilities = probabilities
    
    def __call__(self, n):
        out = [[Person(choice(list(range(len(self.probabilities)))))] if random() < prob else [] for prob in self.probabilities]
        return [floor if floor and floor[0] != i else [] for i, floor in enumerate(out)]


class State:
    def __init__(self, pos=None, passengers=None, house=None, done=None, door_time=10, capacity=5, lifts=None,
                 height=2, max_peps=10):
        self.nestiham = False
        self.vytah = lifts if lifts else 1
        if house is None:
            house = [list() for _ in range(height)]
        if done is None:
            done = []
        if pos is None:
            pos = [[0, 0][:] for _ in range(lifts)]
        if passengers is None:
            passengers = [[][:] for _ in range(lifts)]
        if lifts is None:
            lifts = len(pos)
        self.lifts = lifts
        self.pos = list(pos)
        self.passengers = list(passengers)
        self.house = list(house)
        self.n = len(house)
        self.done = list(done)
        self.door_time = door_time
        self.capacity = capacity
        self.max_peps = max_peps
    
    def add_peps(self, peps):
        for i, floor in enumerate(peps):
            for pep in floor:
                if len(self.get_list()) < self.max_peps:
                    self.house[i].append(pep)
                elif not self.nestiham:
                    print("Nestíhám!!! %d" % len(self.done))
                    self.nestiham = True
                else:
                    pass
    
    def move_up(self, i=0):
        if self.pos[i][1]:
            return self.wait()
            raise ValueError("Cannot move with opened doors.")
        self.pos[i][0] += 1
        if self.pos[i][0] > self.n - 1:
            raise ValueError("Lift went away.")
    
    def move_down(self, i=0):
        if self.pos[i][1]:
            return self.wait()
            raise ValueError("Cannot move with opened doors.")
        self.pos[i][0] -= 1
        if self.pos[i][0] < 0:
            raise ValueError("Lift went away.")
    
    def open_door(self, i=0):
        if self.pos[i][1]:
            return self.wait()
            raise ValueError("Cannot move with opened doors.")
        for j, passenger in enumerate(self.passengers[i]):
            if passenger.where() == self.pos[i][0]:
                self.done.append(passenger)
                del self.passengers[i][j]
        while len(self.passengers[i]) < self.capacity and self.house[self.pos[i][0]]:
            self.passengers[i].append(self.house[self.pos[i][0]][0])
            del self.house[self.pos[i][0]][0]
        
        self.pos[i][1] = self.door_time
        self.wait(i)
    
    def wait(self, i=None):
        if i is None:
            for floor in self.house:
                for pep in floor:
                    pep.tick()
        else:
            self.pos[i][1] = max(self.pos[i][1] - 1, 0)
            for pep in self.passengers[i]:
                pep.tick()
    
    def get_score(self):
        if self.done:
            return sum(map(lambda x: x.get_feedback(), self.done)) / len(self.done)
        else:
            return 0
    
    def get_list(self):
        out = []
        for i, floor in enumerate(self.house):
            for pep in floor:
                out.append((pep, i))
        return out


class Entv:
    def __init__(self, get_new=lambda x: [([] if i else [Person(1)]) for i in range(x)], ticks=10 ** 5, door_time=5,
                 lifts_num=1, height=10, max_peps=100):
        self.get_new = get_new
        self.ticks = ticks
        self.lifts_num = lifts_num
        self.height = height
        self.debug = []
        self.state = None
        self.door_time = door_time
        self.max_peps = max_peps
    
    def test(self, lift):
        self.state = State(lifts=self.lifts_num, height=self.height, door_time=self.door_time, max_peps=self.max_peps)
        reducer = lift.reducer
        for _ in range(self.ticks):
            answer = lift(reducer(self.state))
            self.debug.append(answer)
            for i, answer in enumerate(answer):
                if answer == "down":
                    self.state.move_down(i)
                elif answer == "up":
                    self.state.move_up(i)
                elif answer == "open":
                    self.state.open_door(i)
                elif answer == "wait":
                    self.state.wait(i)
            self.state.wait()
            self.state.add_peps(self.get_new(self.height))
        
        while sum([len(floor) for floor in self.state.house]):
            answer = lift(reducer(self.state))
            for i, answer in enumerate(answer):
                if answer == "down":
                    self.state.move_down(i)
                elif answer == "up":
                    self.state.move_up(i)
                elif answer == "open":
                    self.state.open_door(i)
                elif answer == "wait":
                    self.state.wait(i)
            self.state.wait()
        
        return self.state.get_score()
