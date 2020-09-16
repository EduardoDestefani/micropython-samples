'''
Code PYB_FLC100_IoTServer_v0.3
Authors: Eduardo Destefani Stefanato, Pedro Henrique Robadel & Roberto Colistete Jr.
'''
import socket
import utime
import network
import ure
from ulab import numerical

# Configurating WiFi
ap = network.WLAN(network.AP_IF)
ap.config(essid='FLC100', password='42')
ap.active(True)
print('Ouvindo em', ap.ifconfig()[0])

R1left = 328.8   # in kOhm, voltage divider, left
R2left = 508.7   # in kOhm
R1right = 327.5   # in kOhm voltage divider, right
R2right = 512.3   # in kOhm

adcVref = pyb.ADC(pyb.Pin('Y11'))
adcVplus = pyb.ADC(pyb.Pin('Y12'))
log = open("flc100.csv", "w")
log.write("B(nT), +/-(nT), t(s)\n")

message_counter = 0
NUM_ADC_READINGS = 150
BnTlist = [0.0]*NUM_ADC_READINGS

# Open Web page
try :
    with open('index.html', 'r') as file :
        html = file.read()
except :
    print('Not found files "index.html"')

# Server up
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)
isDownload = False
loop = False

while True :
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)

    while True :
        line = cl_file.readline()
        if not line or line == b'\r\n' :
            if isDownload:
                cl.send(open('flc100.csv').read())
                isDownload = False
            else :            
                cl.send(html)
            break

        if ure.search('GET /\?num=', line) :
            action1 = str(line).split('&')[0].split('=')[1]
            action2 = str(line).split('&')[1].split('=')[1]
            NUM_MEASURES = int(action1)
            TIME_MEASURE = float(action2)

            if NUM_MEASURES and TIME_MEASURE > 0 :
                # EdgComp code
                loop = True
                initialtimems = utime.ticks_ms()
                while loop :
                    for i in range(NUM_ADC_READINGS) :
                        Vplus3V3 = adcVplus.read()*(3.3/4095)
                        Vplus5V = (Vplus3V3*(R1left + R2left))/R2left
                        Vref3V3 = adcVref.read()*(3.3/4095)
                        Vref5V = (Vref3V3*(R1right + R2right))/R2right
                        try :
                            BnTlist[i] = ((Vplus5V - Vref5V)*125000)/Vref5V
                        except ZeroDivisionError :
                            continue

                    timems = utime.ticks_diff(utime.ticks_ms(), initialtimems)
                    BnTmean = numerical.mean(BnTlist)
                    utime.sleep(TIME_MEASURE)
                    BnTstdev = numerical.std(BnTlist)

                    log.write("{}, {}, {}\n".format(BnTmean, BnTstdev, timems//1000))
                    message_counter += 1

                    if message_counter == NUM_MEASURES :
                        log.close()
                        break

        if ure.search('GET /flc100.csv', line) :
            isDownload = True

    cl.close()
    print()