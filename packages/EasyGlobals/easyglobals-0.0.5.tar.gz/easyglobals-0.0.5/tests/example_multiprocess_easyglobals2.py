# from EasyGlobals import EasyGlobals
# import attribute_test as EasyGlobals
from src.EasyGlobals import EasyGlobals
import multiprocessing
globals = EasyGlobals.Globals()

class myclass:
    def __init__(self):
        self.x = 'tset'
        self.z = 'lol'


class myclass2:
    def __init__(self):
        self.x = 2
        self.y = myclass()

tst = myclass2()
print(tst.__dict__)
globals.test4 = tst

# print(globals.test4.y.x)
# print(globals.test4.y.z)
