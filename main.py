from machine import UART, Pin, I2C
import time, onewire, ds18x20, binascii, ssd1306

i2c = I2C(scl=Pin(23), sda=Pin(22), freq=400000)
display=ssd1306.SSD1306_I2C(128,64,i2c)
display.fill(0)
display.show()

led_ext = Pin(17, Pin.OUT)
led_onboard=Pin(2, Pin.OUT)
x = 1
while True:
    uart=UART(1)
    print(x)
    if (uart or x==5):  #el puerto uart0 se usa para USB
        break
    x += 1
    time.sleep(1)
uart.init(115200, bits=8, parity=None, stop=1)
print(uart)
bufer=": "+  str(uart.read())
print(bufer)
display.scroll(0,-8)
display.fill_rect(0,56,128,64,0)
display.show()
display.text(bufer,0,56)
display.show()
time.sleep(10)
bufer=": "+  str(uart.read())
print(bufer)
display.scroll(0,-8)
display.fill_rect(0,56,128,64,0)
display.show()
display.text(bufer,0,56)
display.show()

#modo operación
z=0
retorno="None"
while (z<5 and retorno.find("OK")==-1):
    uart.write(str.encode("at+mode=0\r\n"))
    time.sleep(5)

    x = 0
    while (retorno.find("OK")==-1 and x<5 and retorno.find("ERROR")==-1):
        retorno=str(uart.read())
        print("esperando mode 0 " + retorno + " " + str(z)+ "." + str(x))
        display.scroll(0,-8)
        display.fill_rect(0,56,128,64,0)
        display.show()
        display.text("esperando mode 0 " + retorno + " " + str(z)+ "." + str(x),0,56)
        display.show()
        time.sleep(1)
        x += 1
    z += 1
if (retorno.find("OK")>=0):
    print("conectado")
    display.scroll(0,-8)
    display.fill_rect(0,56,128,64,0)
    display.show()
    display.text("Modulo operativo",0,56)
    display.show()
elif(retorno.find("ERROR")>=0):
    print("error")
    display.scroll(0,-8)
    display.fill_rect(0,56,128,64,0)
    display.show()
    display.text("error",0,56)
    display.show()

##################3
modo="abp"
#####################

if (modo=="otaa"): #otaa
    uart.write(str.encode("at+set_config=app_eui:70B3D57ED001ABFD&app_key:A852247825DA733F16C25B96FA738D8A\r\n"))
elif (modo=="abp"): #abp
    uart.write(str.encode("at+set_config=dev_addr:26011C38&nwks_key:89203CE226AFD40A4F6B3561FF3E9917&apps_key:24136812EC60828FB7AF2CA485F19C41\r\n"))

time.sleep(5)
retorno="eui "+ str(uart.read())
print(retorno)
if (retorno.find("OK")>=0):
    print("conectado")
    display.scroll(0,-8)
    display.fill_rect(0,56,128,64,0)
    display.show()
    display.text("eui "+modo+ " ok",0,56)
    display.show()
elif(retorno.find("ERROR")>=0):
    display.scroll(0,-8)
    display.fill_rect(0,56,128,64,0)
    display.show()
    display.text("eui "+modo+ " error",0,56)
    display.show()

uart.write(str.encode("at+set_config=rx_delay1:6000\r\n"))
time.sleep(2)
print("cambio de delay a 6000ms:  "+ str(uart.read()))

display.fill(0)
display.show()

display.text("join "+modo,0,51)
display.show()

i=0
retorno="None"
print("conectando " + modo)
while (i<5 and retorno.find("OK")==-1):
    uart.write(str.encode("at+join="+ modo +"\r\n"))
    punto=1
    while punto<129:
        display.pixel(punto,63,255)
        display.pixel(punto,62,255)
        display.pixel(punto,61,255)
        display.show()
        time.sleep(.1)
        punto += 1
    retorno=str(uart.read())
    print("intento " + modo + ": " + str(i) +"  "+ retorno)
    display.scroll(0,-5)
    display.fill_rect(0,60,128,4,0)
    display.show()
    i += 1

if (modo=="otaa"):
    if (retorno.find("recv=3")>=0):
        display.scroll(0,-8)
        display.fill_rect(0,56,128,64,0)
        display.show()
        display.text(modo+ "conect ok",0,56)
        display.show()
    else:
        display.scroll(0,-8)
        display.fill_rect(0,56,128,64,0)
        display.show()
        display.text(modo+ "conect NO",0,56)
        display.show()
elif (retorno.find("OK")>=0):
    display.scroll(0,-8)
    display.fill_rect(0,56,128,64,0)
    display.show()
    display.text(modo+ "conect ok",0,56)
    display.show()
else:
    display.scroll(0,-8)
    display.fill_rect(0,56,128,64,0)
    display.show()
    display.text(modo+ "conect NO",0,56)
    display.show()

uart.write(str.encode("at+set_config=rx_delay1:1000\r\n"))
time.sleep(2)
#print("cambio de delay a 1000ms:  "+ str(uart.read()))


ow = onewire.OneWire(Pin(18,Pin.PULL_UP))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
time.sleep(1)
ds.convert_temp()
time.sleep(1)

uart.read()

i=1
while True:
    ds.convert_temp()
    temperatura=(ds.read_temp(roms[0]))
    print(temperatura)
    #valor=int(ds.read_temp(roms[0])*10000)
    #payload=binascii.hexlify(bytes([(valor & 0x00FF00) >> 8 ,(valor & 0x0000FF) ]))
    #send()
    buf=ds.read_scratch(roms[0])
    payload=binascii.hexlify(bytes([buf[1] , buf[0]]))
    print("enviando payload: "+ str(payload))
    uart.write(str.encode("at+send=0,2,") + payload +str.encode("\r\n"))
    time.sleep(10)
    resultado=str(uart.read()) + " ->  " + str(i)
    print(resultado)
    if (resultado.find("recv=2,0")>=0):
        uart.read()
        uart.write(str.encode("at+link_cnt\r\n"))
        led_ext.on()
        time.sleep(1)
        led_ext.off()
        contador=str(uart.read()).split(",")[0].split("K")[1]
        display.fill(0)
        display.show()
        display.text("temp: "+str(temperatura)+"*C",0,0)
        display.text(modo + " Nro: "+ contador,0,10)
        display.show()
    i +=1
    #int(payload[0]<<16) + int(payload[1]<<8) + int(payload[2])
    time.sleep(169)
