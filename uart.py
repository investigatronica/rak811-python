from machine import UART
import time
time.sleep(1)
uart=UART(1) #el puerto uart0 se usa para USB
uart.init(115200, bits=8, parity=None, stop=1)
uart.write(str.encode("at+mode=0\r\n"))

print(uart.write(str.encode("at+get_config=dev_eui\r\n")))
print(uart.readline())
print(str(uart.readline()).split("\\")[0])

print(str(uart.readline()).split("OK")[1].split("\\")[0])
uart.write(str.encode("at+gpio=15,1\r\n"))  #nro de pin del RAK811 LoRa Module y no del beakboard

uart.write(str.encode("at+set_config=app_eui:70B3D57ED001ABFD&app_key:EEAD3B45BF0983C4AAA38A6A3CCB7263\r\n"))
print(uart.readline())
uart.write(str.encode("at+join=otaa\r\n"))
print(uart.readline())

binascii.hexlify(string.encode()).decode("utf-8")

uart.write(str.encode("at+join=otaa\r\n"))
uart.write(str.encode("at+dr=4\r\n"))
uart.write(str.encode("at+send=0,1,63686175\r\n"))
print(uart.read())
uart.write(str.encode("at+set_config=dev_addr:260216A5&nwks_key:39FA09D6D0B4294D5AD52E4722E74ADB&apps_key:F0D377EFC8A38D1C00B340D22F41D42E\r\n"))
uart.write(str.encode("at+join=abp\r\n"))

 (01<<8|int("85",16))/16
