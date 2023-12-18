from random import randint as r


class Helicopter:

    def __init__(self,w,h) -> None:
        self.x = r(0, w-1)
        self.y = r(0,h-1)
        self.tank = 0
        self.max_tank = 1
        self.points = 0
        self.health = 3


    def move(self,st,w,h,m):
        x, y= self.x, self.y
        x0,y0 = x,y
        MOVES = ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
        self.x, self.y = MOVES['dasw'.index(st)]

        try:
            assert 0 <= self.x < w and 0 <= self.y < h, 'ne'
        except Exception:
            self.x, self.y = x0, y0


    def print_stats(self):
        print('💓','x',self.health,'  ','💧', self.tank, '/',self.max_tank,'   ', 'S:',self.points)
