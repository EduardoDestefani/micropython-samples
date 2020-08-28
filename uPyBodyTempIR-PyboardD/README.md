# uPyBodyTempIR-PYBD

Código de interface gráfica para Pyboard-D. Versão mais nova do uPyBodyTempIR para Pyboard-D (uPyBodyTempIR-PYBD_v0.5.py), código produzido para iniciativas contra o [COVID-19](https://gitlab.com/rcolistete/computacaofisica-privado/-/tree/master/uPyBodyTempIR). Tal produção entra nos requisitos propostos pela FAPES, como consta no resumo das atividades de abril ([202004_Atividades](https://github.com/EduardoDestefani/IC-Mag-privado/blob/master/Atividades/202004-12_Atividades_IC_FAPES_especial/202004_Atividades/202004_Atividades.md)).

O resultado, foram quatro versões de códigos funcionais, sendo a v0.5, a mais inteligente, pois utiliza o novo módulo [ulab](https://gitlab.com/rcolistete/micropython-samples/-/blob/master/Pyboard/Firmware/v1.12_with_ulab/ulab_v0.54.0_2020-07-26/Pyboard_D_SF2W/pybd-sf2_ulab_sp_v1.12-662-gf8531fe04_2020-07-26.dfu) e menos linhas. Todas as versões estão disponíveis em; https://gitlab.com/rcolistete/computacaofisica-privado/-/tree/master/uPyBodyTempIR/uPyBodyTempIR-PyboardD



Veja o código principal (v0.5) abordado a seguir:

```python
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
```
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



## Etapas de Funcionamento

O código funciona de acordo com os seguintes parâmetros; coleta de medidas, armazenamento e processamento dos dados. Isso é feito de acordo com o estímulo escolhido, que no caso, foi pressionar o botão USR do Pyboard-D, simulando o que seria um sensor de proximidade. Daí as etapas são:



#### Ociosidade
Nesta etapa, o microcontrolador (Pyboard-D) espera um estímulo externo que o faça executar a coleta de dados. Nesse caso, ele aguarda que o botão USR seja pressionado. Enquanto isso, ele apresenta uma mensagem "Esperando proximidade ...".



#### Coleta de dados
Nesta etapa, o botão é pressionado, simulando uma pessoa perto, e o microcontrolador começa a coletar as medidas fornecidas da função principal. Todos os valores que estejam no intervalo pré-estabelecido no script serão armazenados em uma lista de 8 valores. Caso esses valores atendam os critérios do intervalo proposto, o microcontrolador parte para a próxima etapa. Durante a coleta de dados o microcontrolador apresenta uma mensagem escrita "Carregando ...", junto a um LED verde. Caso a pessoa se afaste durante o processo de coleta de dados, o microcontrolador pede para que a mesma "Se aproxime!" junto a um LED vermelho, se a pessoa afastou-se diversas vezes da zona de medida, um total igual a 8 valores, o Pyboard mostra uma mensagem dizendo "Não há alguém próximo." e pula para a etapa de **Pós processamento**. Isso é feito para evitar um grande desvio padrão na temperatura final na etapa **Processamento de dados**.



#### Processamento de dados
Nesta etapa, o microcontrolador executa uma análise estatística da lista de 8 valores, tirando média e desvio padrão da mesma. Caso cada um dos valores estejam dentro do intervalo da média +/- o desvio padrão, o microcontrolador fornece a medida dizendo "Medida feita!", a temperatura e o resultado (Normal, Febre, Febre Alta e Hipertermia). Caso as medidas não estejam de acordo, ele pede para que a pessoa tente novamente e indica que a mesma pode ter se afastado com uma mensagem "Não há alguém próximo.", dito anteriormente.



#### Pós processamento
Nesta etapa, o microcontrolador já analisou e indicou a temperatura da pessoa, em seguida ele executa um comando de delay (atraso) dizendo "Aguarde ..." e apaga os dados para uma próxima medida.