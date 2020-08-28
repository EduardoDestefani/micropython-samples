'''
Interface gráfica uPyBodyTempIR-MicroBit.
Autores: Eduardo Destefani, Diego Santos de Jesus & Roberto Colistete Jr.
'''
from microbit import *
import mlx90615 as mlx
import math
import time

MIN_ACCEPTABLE = 3400 # (34.00 C)
MAX_ACCEPTABLE = 4200 # (42.00 C)
TIME_BETWEEN_MEASUREMENTS = 0.5 # 500 ms = 0.500 s
NUM_MEASUREMENTS = 8
TIME_AFTER_MEASUREMENTS = 7 # 7000 ms = 7.000 s

def mean(data):
    if iter(data) is data:
        data = list(data)
    return sum(data)/len(data)

def stdev(data, xbar=None):
    if iter(data) is data:
        data = list(data)
    if xbar is None:
        xbar = sum(data)/len(data)
    total = total2 = 0
    for x in data:
        total += (x - xbar)**2
        total2 += (x - xbar)
    total -= total2**2/len(data)
    return math.sqrt(total/(len(data) - 1))

display.scroll('Oi, eu sou o uPyBodyTempIR-MicroBit', delay=110, wait=True) # start's software
flag_exit = False

while True:

    while (not flag_exit):
        if accelerometer.was_gesture('face up'): # estímulo que indica a presença de uma pessoa/objeto perto do protótipo
        	display.show(Image.HAPPY, delay=1500, clear=True)
        	display.scroll('Fique a 3cm da tela.', delay=110, wait=True)
        	time.sleep(2)
        	display.scroll('Fique Parado!', delay=120, wait=True)
        	break
    	elif button_b.was_pressed(): # button_b seria como um estímulo substituto a presença detectada por um sensor de proximidade ou de tempeatura
        	display.show(Image.SAD, delay=1000, clear=True)
        	flag_exit

	count = 0
	lst_Temp = []
	lst_Tambient = []
    while (not flag_exit):
        mlx.Read_MLX90615_Temperatures()
    	time.sleep(TIME_BETWEEN_MEASUREMENTS)

    	if button_b.was_pressed(): # button_b seria como um estímulo substituto ao tipo de presença detectada por um sensor de proximidade ou de tempeatura
        	display.show(Image.SAD, delay=1000, clear=True) # a pessoa de afastou :(
        	flag_exit
    	elif (not button_b.was_pressed()):
            if (MIN_ACCEPTABLE <= mlx.Read_MLX90615_Temperatures()[0] <= MAX_ACCEPTABLE) and (not flag_exit):
            	lst_Temp.append(mlx.Read_MLX90615_Temperatures())
            	count += 1
            	display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)
            	if (count == NUM_MEASUREMENTS):
                	break
            else:
            	lst_Tambient.append(mlx.Read_MLX90615_Temperatures())

    if (count == NUM_MEASUREMENTS) and (not flag_exit):
    	lst_object = [i[0]/100 for i in lst_Temp]
    	lst_ambient = [i[0]/100 for i in lst_Tambient]

    	lst_Tobject = list(zip(lst_object, lst_ambient)) # lista de tuplas (temperatura do objeto, temperatura do ambiente)
    	objt_mean = mean(lst_object) # indica a média da temperatura da pessoa/objeto
    	objt_stdev = stdev(lst_object) # desvio padrão

    watchmen = 0
    for i in lst_object:
        if (objt_mean - objt_stdev <= i <= objt_mean + objt_stdev):
            watchmen += 1
            if watchmen == NUM_MEASUREMENTS:
                display.show(Image.DIAMOND, delay=1000, wait=True, clear=True)
        else:
            display.show(Image.NO, delay=1500, clear=True)
            display.scroll('Tente de novo!', delay=120, wait=True)

    if (objt_mean - objt_stdev <= i <= objt_mean + objt_stdev) and (watchmen == NUM_MEASUREMENTS):
    	display.scroll('{} +/- {} C'.format(objt_mean, objt_stdev), delay=150, wait=True)
    	time.sleep(1)

    	if (37.8 <= objt_mean < 39.6):
        	display.scroll('Febre.', delay=130, wait=True)
    	elif (39.6 <= objt_mean < 41):
        	display.scroll('Febre Alta.', delay=130, wait=True)
    	elif (objt_mean >= 41):
        	display.scroll('Hipertermia!', delay=130, wait=True)
    	else:
        	display.scroll('Normal.', delay=130, wait=True)

    	time.sleep(4)
    	display.scroll('Fim.', delay=120, wait=True)
    	display.scroll('Se afaste.', delay=120, wait=True)
        time.sleep(TIME_AFTER_MEASUREMENTS)

    while (mlx.Read_MLX90615_Temperatures()[0] >= MIN_ACCEPTABLE) and (not flag_exit):
    	mlx.Read_MLX90615_Temperatures()
    	time.sleep(TIME_BETWEEN_MEASUREMENTS)
    	if (mlx.Read_MLX90615_Temperatures()[0] < MIN_ACCEPTABLE):
        	break
    	elif button_b.was_pressed():
        	flag_exit

	lst_Temp = []
	lst_Tambient = []
	lst_object = []