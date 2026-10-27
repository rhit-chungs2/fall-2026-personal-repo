import gpiozero as gz
import time

class Ultrasonic:
    def __init__(self):
        self.sensor = gz.DistanceSensor(echo = 22, trigger = 27)
        

    def get_cm(self):
        return round(self.sensor.distance * 100,1)

class LineSensors:
    def __init__(self):
        self.left = gz.LineSensor(14)
        self.middle = gz.LineSensor(15)
        self.right = gz.LineSensor(24)

    def get_left(self):
        # 0 is White
        # 1 is Black
        if self.left.value == 1:
            return "B"
        return "W"

    def get_middle(self):
        # 0 is White
        # 1 is Black
        if self.left.value == 1:
            return "B"
        return "W"

    def get_right(self):
        # 0 is White
        # 1 is Black
        if self.left.value == 1:
            return "B"
        return "W"
    
    def get_line_word(self):
        return self.get_left() + self.get_middle() + self.get_right()


if __name__ =="__main__":
    print("Quick deve testing for sensors!")
    ultra = Ultrasonic()
    line_sensors = LineSensors()

    while True:
        #print(line_sensors.get_line_word())
        print(ultra.get_cm())

        time.sleep(1)