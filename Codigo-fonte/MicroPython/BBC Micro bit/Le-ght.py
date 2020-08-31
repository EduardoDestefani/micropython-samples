'''
Game Name : Le-ght (a left and right game to test your reflex)
Author : Eduardo Destefani Stefanato (c)
Student's Federal University of Espírito Santo
Play on BBC Micro:bit
'''
from microbit import *
from random import randrange

loop = False

def coin():
    global count
    if randrange(100) % 2 == 0 :
        return 1
    else :
        return 0

# Select
display.show(Image.DIAMOND, delay=1000, wait=True, clear=True)
display.scroll('Select difficulty', delay=110, wait=True)
display.scroll('Press B', delay=110, wait=True)
difficulty = 0
while True :
    if button_b.get_presses() :
        difficulty += 1
        display.show(difficulty, wait=True, clear=False)
        if difficulty >= 5 :
            display.show(Image.NO, delay=400)
            difficulty = 0
    elif button_a.get_presses() :
        if difficulty == 0 :
            reset()
        display.show(Image.HAPPY, delay=1000, wait=True, loop=False, clear=True)
        difficulty
        loop = True
        break

# Start
while loop :
    display.scroll('Press B to start', delay=110, wait=True)
    display.show(Image.ARROW_E, delay=1000, clear=True)
    reflex = difficulty*100

    if difficulty == 4 :
        points = 20
    elif difficulty == 3 :
        points = 15
    elif difficulty == 2 :
        points = 12
    elif difficulty == 1 :
        points = 10

    if button_b.was_pressed() :
        time = 0
        wathmen = 0
        while True :
            coin()
            if coin() == 1 :
                display.show(Image.ARROW_W, delay=(2000 - time), clear=True)
                if button_a.get_presses() :
                    time = randrange(0, 1800, reflex)
                    wathmen += 1
                    if wathmen == points :
                        display.scroll('Game Won!', delay=100, wait=True)
                        break
                elif button_b.get_presses() :
                    display.show(Image.NO, delay=1000, clear=True)
                    display.scroll('{} points'.format(wathmen), delay=150, wait=True)
                    break
            elif coin() == 0 :
                display.show(Image.ARROW_E, delay=(2000 - time), clear=True)
                if button_b.get_presses() :
                    time = randrange(0, 1800, reflex)
                    wathmen += 1
                    if wathmen == points :
                        display.scroll('Game Won!', delay=100, wait=True)
                        break
                elif button_a.get_presses() :
                    display.show(Image.NO, delay=1000, clear=True)
                    display.scroll('{} points'.format(wathmen), delay=150, wait=True)
                    break


