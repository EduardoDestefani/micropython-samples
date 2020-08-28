'''
Interface gráfica uPyBodyTempIR-PyboardD.
Autores: Eduardo Destefani & Roberto Colistete Jr.
'''
from pyb import Switch
from ulab import numerical
from time import sleep
import mlx90615 as mlx

MIN_TEMP_ACCEPT = 3400 # (34.00 C)
MAX_TEMP_ACCEPT = 4200 # (42.00 C)
TIME_MS_BETWEEN_TEMP_MEASUREMENTS = 0.5 # 500 ms = 0.500 s
NUM_TEMP_MEASURE = 8
TIME_MS_AFTER_TEMP_MEASUREMENTS = 7 # 7000 ms = 7.000 s
# start's software

flag_exit = False
sw = Switch()
sw.value() # returns True or False

while True:
    print('\nEsperando proximidade ...', end='')
    while (not flag_exit):
        if sw.value() == True: # estímulo que indica a presença de uma pessoa/objeto perto do protótipo
            pyb.LED(2).on()
            print('\nOi, eu sou o uPyBodyTempIR-PYBD_v0.4\n')
            print('Fique a 3cm da tela.')
            sleep(2)
            print('Fique Parado!\n')
            break
        else:
            pyb.LED(2).off()
            print('.',end='')
            sleep(1)
            flag_exit

    count = 0
    prox = 0
    lst_Temp = []
    lst_Tambient = []
    while (not flag_exit):
        mlx.Read_MLX90615_Temperatures()
        sleep(TIME_MS_BETWEEN_TEMP_MEASUREMENTS)

        if sw.value() == False: # button_USR análogo a um sensor de proximidade ou de temperatura
            pyb.LED(2).off()
            pyb.LED(1).on()
            print('Se aproxime!')
            sleep(1)
            prox += 1
            if prox == NUM_TEMP_MEASURE:
                print('\nNão há alguém próximo.\n')
                prox = 0
                break
        else:
            if (MIN_TEMP_ACCEPT <= mlx.Read_MLX90615_Temperatures()[0] <= MAX_TEMP_ACCEPT) and (not flag_exit):
                pyb.LED(1).off()
                pyb.LED(2).on()
                lst_Temp.append(mlx.Read_MLX90615_Temperatures())
                count += 1
                print('Carregando ...')
                if (count == NUM_TEMP_MEASURE):
                    break
            else:
                lst_Tambient.append(mlx.Read_MLX90615_Temperatures())

    if (count == NUM_TEMP_MEASURE) and (not flag_exit):
        lst_object = [i[0]/100 for i in lst_Temp]
        lst_ambient = [i[0]/100 for i in lst_Tambient]

        lst_Tobject = list(zip(lst_object, lst_ambient)) # lista de tuplas (temp do objeto, temp do ambiente)
        obj_mean = numerical.mean(lst_object) # indica a média da temperatura da pessoa/objeto
        obj_std = numerical.std(lst_object) # desvio padrão

    if (count == NUM_TEMP_MEASURE) and (not flag_exit):
        
        pyb.LED(2).on()
        watchmen = 0
        for i in lst_object:
            if (obj_mean - obj_std <= i <= obj_mean + obj_std):
                watchmen += 1
                if watchmen == NUM_TEMP_MEASURE:
                    print('\nMedida feita!')
        if watchmen != NUM_TEMP_MEASURE:
            pyb.LED(2).off()
            pyb.LED(1).on()
            print('\nVocê pode ter se afastado ...')
            print('Tente de novo!\n')

    if (count == NUM_TEMP_MEASURE) and (not flag_exit):
        if (obj_mean - obj_std <= i <= obj_mean + obj_std) and (watchmen == NUM_TEMP_MEASURE):
            print('{} +/- {} C'.format(obj_mean, obj_std))
            sleep(1)

            if (37.8 <= obj_mean < 39.6):
                pyb.LED(1).on()
                print('Febre.')
            elif (39.6 <= obj_mean < 41):
                pyb.LED(1).on()
                print('Febre Alta.')
            elif (obj_mean >= 41):
                pyb.LED(1).on()
                print('Hipertermia!')
            else:
                pyb.LED(2).on()
                print('Normal.')

            sleep(2)
            print('\nFim.')
            print('Se afaste.\n')
            sleep(TIME_MS_AFTER_TEMP_MEASUREMENTS)

    pyb.LED(1).off()
    print('Aguarde ...', end='')
    while (mlx.Read_MLX90615_Temperatures()[0] >= MIN_TEMP_ACCEPT) and (not flag_exit):
        mlx.Read_MLX90615_Temperatures()
        print('.', end='')
        sleep(1)
        if (mlx.Read_MLX90615_Temperatures()[0] < MIN_TEMP_ACCEPT):
            break
        elif sw.value() == False:
            flag_exit

    lst_Temp = []
    lst_Tambient = []
    lst_object = []