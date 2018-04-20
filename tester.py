from algoritmy import BasicLift, MinDistLift, MinDistCollect, RandomLift
from multiElev import MultiElev
from prostredi import Entv, Generator

env = Entv(get_new=Generator([0.001] + ([0.0001]*99)), height=100, door_time=10, ticks=10**5)
print(env.test(RandomLift()))
print(env.test(BasicLift()))
print(env.test(MinDistLift()))
print(env.test(MinDistCollect()))
#print(env.test(MultiElev()))
