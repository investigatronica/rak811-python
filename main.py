from machine import UART, Pin
import time, onewire, ds18x20, binascii
x = 1

while True:
    uart=UART(1)
    print(x)
    if (uart or x==5):  #el puerto uart0 se usa para USB
        break
    x += 1
    time.sleep(1)
print("uart= "+  str(uart))
uart.init(115200, bits=8, parity=None, stop=1)
print(str(uart.read()))
print(str(uart.read()))
print(str(uart.read()))
time.sleep(10)

#uart.write(str.encode("at+reset=0\r\n"))
time.sleep(5)
#print("reset: " + str(uart.read()))

z=0
retorno="None"

#modo operación
while (z<5 and retorno.find("OK")==-1):
    uart.write(str.encode("at+mode=0\r\n"))
    time.sleep(1)

    x = 0
    while (retorno.find("OK")==-1 and x<5 and retorno.find("ERROR")==-1):
        retorno=str(uart.read())
        print(retorno + " " + str(z)+ "." + str(x))
        time.sleep(1)
        x += 1
    z += 1
if (retorno.find("OK")>=0):
    print("conectado")
elif(retorno.find("ERROR")>=0):
    print("ERROR")

#uart.write(str.encode("at+set_config=app_eui:70B3D57ED001ABFD&app_key:EEAD3B45BF0983C4AAA38A6A3CCB7263\r\n"))
uart.write(str.encode("at+set_config=dev_addr:260216A5&nwks_key:39FA09D6D0B4294D5AD52E4722E74ADB&apps_key:F0D377EFC8A38D1C00B340D22F41D42E\r\n"))
time.sleep(5)
print("eui "+ str(uart.read()))

ow = onewire.OneWire(Pin(18,Pin.PULL_UP))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

#falta ponerlo en un while
time.sleep(5)
print("enviando abp")
#uart.write(str.encode("at+join=otaa\r\n"))
uart.write(str.encode("at+join=abp\r\n"))
time.sleep(5)
print("abp 1: "+ str(uart.read()))
time.sleep(5)
print("abp 2: "+ str(uart.read()))
time.sleep(5)
print("abp 3: "+ str(uart.read()))
time.sleep(5)
print("abp 4: "+ str(uart.read()))

i=0
while True:
    ds.convert_temp()
    #print(ds.read_temp(roms[0]))
    #valor=int(ds.read_temp(roms[0])*10000)
    #payload=binascii.hexlify(bytes([(valor & 0x00FF00) >> 8 ,(valor & 0x0000FF) ]))
    #send()
    buf=ds.read_scratch(roms[0])
    payload=binascii.hexlify(bytes([buf[1] , buf[0]]))
    uart.write(str.encode("at+send=0,2,") + payload +str.encode("\r\n"))
    time.sleep(10)
    print(str(uart.read()) + " ->  " + str(i))
    i +=1
    #int(payload[0]<<16) + int(payload[1]<<8) + int(payload[2])
    time.sleep(110)
