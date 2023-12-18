from pynput import keyboard
import os
import json
from time import sleep
from map import Map
from helicopter import Helicopter

HEIGTH = 10
WIDTH = 30
TICK = 1
FPS = 45
FIRE_FREQ = 5
CLOUDS = 20
THUNDER = 20

m_bay = Helicopter(WIDTH,HEIGTH)

test1 = Map(HEIGTH,WIDTH)
test1.gen_riv(int(HEIGTH*WIDTH*0.1))
test1.gen_tree(int(HEIGTH*WIDTH*0.3))
test1.gen_workshop()
test1.gen_hospital()

def process(m_bay,m):
    if m.map[m_bay.y][m_bay.x] == 3:
        m_bay.tank = m_bay.max_tank
    elif m.map[m_bay.y][m_bay.x] == 4 and m_bay.tank > 0:
        m_bay.tank -= 1
        m_bay.points += 1000
        del m.burn_list[(m_bay.y,m_bay.x)]
        m.map[m_bay.y][m_bay.x] = 1
    elif m.map[m_bay.y][m_bay.x] == 6 and m_bay.points >= 20000 and m_bay.max_tank < 3:
        m_bay.points -= 20000
        m_bay.max_tank +=1
    elif m.map[m_bay.y][m_bay.x] == 7 and m_bay.points >= 10000:
        m_bay.points -= 10000
        m_bay.health +=1
    elif (m_bay.y,m_bay.x) in m.thunder:
        m_bay.health -= 1
        if m_bay.health < 1:
            os.system('cls')
            print('GAME OVER')
            print('ur score:',m_bay.points)
            exit(0)


def save():
    save_data = {'helicopter':{
                    'hp': m_bay.health,
                    'tank': m_bay.tank,
                    'm_tank': m_bay.max_tank,
                    'points': m_bay.points,
                    'y': m_bay.y,
                    'x': m_bay.x},
                'map':{
                    'm':test1.map,
                    'b':test1.burn_list,
                    'c':test1.clouds,
                    't':test1.thunder},
                'tick':TICK}
    with open('save.json','w') as save:
        json.dump(save_data, save)


def load():
    with open('save.json','r') as sav:
        data = json.load(sav)
        m_bay.health = data['helicopter']['hp']
        m_bay.tank = data['helicopter']['tank']
        m_bay.max_tank = data['helicopter']['m_tank']
        m_bay.points = data['helicopter']['points']
        m_bay.y = data['helicopter']['y']
        m_bay.x = data['helicopter']['x']
        test1.map = data['map']['m']
        test1.burn_list = data['map']['b']
        test1.clouds = data['map']['c']
        test1.thunder = data['map']['t']
        TICK = data['tick']

def on_release(key):
    if type(key) == keyboard._win32.KeyCode:
        t = key.char.lower()
        if t in 'wasd':
            m_bay.move(t,WIDTH,HEIGTH,test1)
            process(m_bay,test1)
        elif t == 'j':
            save()
        elif t == 'l':
            load()

listener = keyboard.Listener(
    on_press=None,
    on_release=on_release)
listener.start()


while True:
    os.system('cls')
    print(TICK)
    m_bay.print_stats()
    test1.print_map(m_bay)
    print('$💓 - 10000        $💧 - 20000')
    if TICK % (FPS*FIRE_FREQ) == 0:
        test1.gen_fire(T=TICK)
    if TICK % (FPS*FIRE_FREQ*2) == 0:
        test1.gen_tree()
    if TICK % FPS == 0:
        test1.burned(T=TICK,F=FPS,m_bay=m_bay)
        test1.gen_clouds(CLOUDS)
        test1.gen_thunder(THUNDER)
        process(m_bay,test1)
    TICK += 1
    sleep(1/FPS)
