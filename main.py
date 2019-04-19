from machine import UART, Pin
import time, onewire, ds18x20
x = 1

while True:
    uart=UART(1)
    print(x)
    if (uart or x==10):  #el puerto uart0 se usa para USB
        break
    x += 1
    time.sleep(1)
print(uart)
uart.init(115200, bits=8, parity=None, stop=1)

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
if (retorno.find("OK")>=0)):
    print("conectado")
elif(retorno.find("ERROR")>=0)
    print("ERROR")

ow = onewire.OneWire(Pin(18,Pin.PULL_UP))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

#falta ponerlo en un while
uart.write(str.encode("at+join=otaa\r\n"))

while True:
    ds.convert_temp()
    print(ds.read_temp(roms[0]))
    valor=int(ds.read_temp(roms[0])*10000)
    payload=bytearray([(valor & 0xFF0000) >> 16 ,(valor & 0x00FF00) >> 8 ,(valor & 0x0000FF) ])
    #send()
    #int(payload[0]<<16) + int(payload[1]<<8) + int(payload[2])
    time.sleep(60)
