import Starfive.GPIO as GPIO
import time
import sys

def main():
    ret = GPIO.SensorCheck()
    if (ret < 0):
        print("Sensor isn't exit ! \n")
        return ret

    GPIO.softreset()

    while True:
        tem = GPIO.getTem()
        hum = GPIO.getHum()
        print("Temperature = {:.2f}°C, Humidity = {:.2f} \n".format(tem, hum))
        time.sleep(1)

if __name__ == "__main__":
    sys.exit(main())
