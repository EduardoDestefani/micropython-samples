'''
Game Name : D-Bit (a RPG dice for BBC Micro:bit)
Author : Eduardo Destefani Stefanato (c)
Student's Federal University of Espírito Santo
Play on BBC Micro:bit

option 1 = D2 | option 2 = D4 | option 3 = D6 | option 4 = D8 | option 5 = D10 | option 6 = D20 | option 7 = D100
'''
from microbit import *
from random import randint
from machine import reset

def d2():
    return randint(1,2)
def d4():
    return randint(1,4)
def d6():
    return randint(1,6)
def d8():
    return randint(1,8)
def d10():
    return randint(1,10)
def d20():
    return randint(1,20)
def d100():
    return randint(1,100)

loop = False

option = 0
display.show(Image.DIAMOND, delay=1000, wait=True, clear=True)
display.show(Image.ARROW_E, delay=1000, clear=True)

while True :
    if button_b.get_presses() :
        option += 1
        display.show(option, wait=True, clear=False)
        if option >= 8 :
            display.show(Image.NO, delay=1000)
            option = 0
    elif button_a.get_presses() :
        if option == 0 :
            reset()
        display.show(Image.HAPPY, delay=1000, wait=True, loop=False, clear=True)
        option
        loop = True
        break

display.scroll('Shake', delay=90, wait=True)
while loop :
    value = d2()
    while option == 1 :
        if accelerometer.was_gesture('shake') :
            display.scroll('D2={}'.format(value), delay=120)
        elif button_a.get_presses() :
            reset()
    value = d4()
    while option == 2 :
        if accelerometer.was_gesture('shake') :
            display.scroll('D4={}'.format(value), delay=120)
        elif button_a.get_presses() :
            reset()
    value = d6()
    while option == 3 :
        if accelerometer.was_gesture('shake') :
            display.scroll('D6={}'.format(value), delay=120)
        elif button_a.get_presses() :
            reset()
    value = d8()
    while option == 4 :
        if accelerometer.was_gesture('shake') :
            display.scroll('D8={}'.format(value), delay=120)
        elif button_a.get_presses() :
            reset()
    value = d10()
    while option == 5 :
        if accelerometer.was_gesture('shake') :
            display.scroll('D10={}'.format(value), delay=120)
        elif button_a.get_presses() :
            reset()
    value = d20()
    while option == 6 :
        if accelerometer.was_gesture('shake') :
            display.scroll('D20={}'.format(value), delay=120)
        elif button_a.get_presses() :
            reset()
    value = d100()
    while option == 7 :
        if accelerometer.was_gesture('shake') :
            display.scroll('D100={}'.format(value), delay=120)
        elif button_a.get_presses() :
            reset()
