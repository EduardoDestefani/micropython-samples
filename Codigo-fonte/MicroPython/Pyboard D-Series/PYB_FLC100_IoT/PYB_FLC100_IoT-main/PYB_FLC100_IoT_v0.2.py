'''
This is a Pyboard-D SF2W's software for reading's magnet field with sensor fluxgate FLC100.
Authors; Eduardo Destefani Stefanato, Roberto Colistete Júnior and Pedro Henrique Robadel da Silva Câmara. 
'''
from ulab import numerical
import network
import thingspeak
from time import sleep

# IOT_BEGIN
# WIFI-CONFIG

SSID="Leninha"
PWD="1220leninha"

sta = network.WLAN(network.STA_IF)
sta.active(1)
sta.active(True)
sta.connect(SSID, PWD) # Necessário alterar ssid e senha para diferente wifi

print("Conectando na '{}' ...".format(SSID),end="")

while not sta.isconnected():
    print(".", end="")
    sleep(1)

print("\nConectado na rede {}!".format(SSID))

ts = thingspeak.Thingspeak()
ts.openConnection()

print("Conectado ao Thingspeak!")

# END_IOT

from ulab import numerical
import utime

NUM_ADC_READINGS = 150
NUM_MEASURES = int(input('Num. de medidas : '))
TIME_BETWEEN_MEASURES = int(input('Atraso (min. 20s): '))
R1left = 328.8   # in kOhm, voltage divider, left
R2left = 508.7   # in kOhm
R1right = 327.5   # in kOhm voltage divider, right
R2right = 512.3   # in kOhm

adcVref = pyb.ADC(pyb.Pin('Y11'))
adcVplus = pyb.ADC(pyb.Pin('Y12'))

log = open("flc100.txt", "w")
log.write("B(nT), t(s)\n")

message_counter = 1
loop = True
initialtimems = utime.ticks_ms()

BnTlist = [0.0]*NUM_ADC_READINGS

while loop:
    # FLC 100 using voltage divider, mean of NUM_ADC_READINGS of Pyboard D internal ADC (12 bits) :

    for i in range(NUM_ADC_READINGS):
        Vplus3V3 = adcVplus.read()*(3.3/4095)
        Vplus5V = (Vplus3V3*(R1left + R2left))/R2left
        Vref3V3 = adcVref.read()*(3.3/4095)
        Vref5V = (Vref3V3*(R1right + R2right))/R2right
        try:
            BnTlist[i] = ((Vplus5V - Vref5V)*125000)/Vref5V # 125000 nT = (50*1000 nT)*Vref (aprox. 2.50V)
        except ZeroDivisionError:
            continue
    # Data processing:

    # Mensures every TIME_BETWEEN_MEASURES in secunds
    timems = utime.ticks_diff(utime.ticks_ms(), initialtimems)
    BnTmean = numerical.mean(BnTlist)
    utime.sleep(TIME_BETWEEN_MEASURES)
    BnTstdev = numerical.std(BnTlist)

    log.write("{}, {}\n".format(BnTmean, timems//1000))
    ts.uploadData(message_counter, BnTmean, BnTstdev,max(BnTlist), min(BnTlist))
    print('#{}, B mean = {:f} nT, delta B = {} nT, max = {}, min = {}'.format(message_counter, BnTmean, BnTstdev, max(BnTlist), min(BnTlist)))
    message_counter += 1

    if message_counter == NUM_MEASURES: # número medidas
        log.close()
        break