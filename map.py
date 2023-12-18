from random import randint as r



CELLS = '⬛🌳⬜🚰🔥🚁🏠💟⚡'


class Map:
    x = 10
    y = 10
    burn_list = {}

    def __init__(self,y,x):
        self.y = y
        self.x = x
        self.map = [[0 for i in range(self.x)] for j in range(self.y)]
        self.clouds = []
        self.thunder = []



    def gen_riv(self,riv_l=10):
        x, y = r(0, self.x-1), r(0, self.y-1)
        if self.map[y][x] == 0:
            self.map[y][x] = 3
            riv_l-=1
            k=100
        while riv_l > 0 and k>0:
            k-=1
            MOVES = ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
            x0,y0 = x,y
            try:
                x,y = MOVES[r(0,3)]
                assert self.map[y][x] == 0, 'ZANAYTO'
                self.map[y][x] = 3
                riv_l-=1
            except Exception:
                x,y = x0, y0


    def gen_tree(self,tree_count=1):
        while tree_count > 0:
            try:
                x, y = r(0, self.x-1), r(0, self.y-1)
                assert self.map[y][x] == 0, 'NO'
                self.map[y][x] = 1
            except Exception:
                continue
            else:
                tree_count -= 1


    def gen_fire(self, fire_count=1,T=1):
        fire_count = fire_count * r(0,3)
        try_count = 50*fire_count
        while fire_count > 0 and try_count> 0:
            try_count -= 1
            x, y = r(0, self.x-1), r(0, self.y-1)
            if self.map[y][x] == 1:
                self.map[y][x] = 4
                self.burn_list[(y,x)] = T
                fire_count -=1


    def burned(self,T,F,m_bay):
        temp = []
        for i in self.burn_list:
            if self.burn_list[i] < T - F*5:
                self.map[i[0]][i[1]] = 0
                temp.append(i)
                m_bay.points -= 333
        for i in temp:
            del self.burn_list[i]


    def gen_workshop(self):
        count = 1
        while count > 0:
            x, y = r(0, self.x-1), r(0, self.y-1)
            if self.map[y][x] == 1:
                self.map[y][x] = 6
                count -= 1


    def gen_hospital(self):
            count = 1
            while count > 0:
                x, y = r(0, self.x-1), r(0, self.y-1)
                if self.map[y][x] == 1:
                    self.map[y][x] = 7
                    count -= 1


    def gen_clouds(self,c):
        if r(0,99) < c:
            x, y = r(0, self.x-1), r(0, self.y-1)
            self.clouds.append((y, x))
            if len(self.clouds) > 3:
                del self.clouds[0]


    def gen_thunder(self,t):
        if r(0,99) < t:
            x, y = r(0, self.x-1), r(0, self.y-1)
            self.thunder.append((y, x))
            if len(self.thunder) > 3:
                del self.thunder[0]


    def print_map(self, m_bay):
        print(*[CELLS[2] for _ in range(self.x + 2)], sep='')
        for i in range(0, self.y):
            print(CELLS[2], end='')
            for j in range(0, self.x):
                if (i, j) in self.thunder:
                    print(CELLS[8],end='')
                elif (i, j) in self.clouds:
                    print(CELLS[2], end='')
                elif m_bay.y == i and m_bay.x == j:
                    print(CELLS[5],end='')
                else:
                    print(CELLS[self.map[i][j]], end='')
            print(CELLS[2], end='')
            print()
        print(*[CELLS[2] for _ in range(self.x + 2)], sep='')
