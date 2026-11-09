import mqtt_helper as mh
import signal
import time
from rosebot import Rosebot
import datetime


class App:
    def __init__(self):
        self.robot = Rosebot()
        self.is_streaming = True 
        self.mode = "none"

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="ME435/#",
                                 publish_topic_name= "ME435/jason/to_computer")
        self.mqtt_client.callback = self.mqtt_callback

    def mqtt_callback(self, message_type, message_payload):
        print("Recieved type:", message_type)
        print("Recieved payload:", message_payload)

        if message_type == "set_speeds":
            self.robot.drive_system.set_speeds(message_payload[0],message_payload[1],message_payload[2],message_payload[3])

        if message_type == "stop":
            self.robot.drive_system.set_speeds(0, 0, 0, 0)        
        if message_type == "beep":
            self.robot.buzzer.beep(on_time=0.1, off_time=0.3, n =2)
        if message_type == "is_streaming":
            self.is_streaming = message_payload
        if message_type == "mode":
            self.mode = message_payload
            if self.mode == "drive_unitl_wall" or self.mode == "drive_until_line":
                self.robot.drive_system.go(20,20)
            if self.mode == "none":
                self.robot.drive_system.stop()
        
def main():
    print("Car MQTT")

    app = App()
    last_time_sent_s = 0


    #Talking to myself
    time.sleep(2)
    #app.mqtt_client.send_message("is_streaming", True)
    app.mqtt_client.send_message("mode", "drive_unitl_wall")

    try:

         while True:
            right_now = datetime.datetime.now()
            current_time_s = right_now.timestamp()
            #print(current_time_s)
            #Strategy is to look at the clock, if two seconds have passed do something.
            if app.is_streaming and current_time_s>last_time_sent_s + 2.0:
                last_time_sent_s = current_time_s
                app.mqtt_client.send_message("Line_sensor_reading",{
                    "timestamp": right_now.strftime("%m/%d/%Y %H:%M:%S"),
                    "left": app.robot.line_sensor.get_left(),
                    "middle": app.robot.line_sensor.get_middle(),
                    "right": app.robot.line_sensor.get_right(),

                      })
                if app.mode == "drive_unitl_wall":
                    #check for wall
                    if app.robot.ultrasonic.get_cm() < 20:
                        app.robot.drive_system.stop()
                        app.robot.buzzer.beep(on_time= 0.1, off_time = 0.1, n=3)
                        app.mode = "none"
                if app.mode == "drive_until_line":
                    if app.robot.line_sensor.get_left() == "B" and app.robot.line_sensor.get_middle() == "B" and app.robot.line_sensor.get_right() == "B":
                        app.robot.drive_system.stop()
                        app.robot.buzzer.beep(on_time= 0.1, off_time = 0.1, n=3)
                        app.mode = "none"
        #     #Send test messages
        #     app.mqtt_client.send_message("beep")
        #     time.sleep(2)
        #     app.mqtt_client.send_message("stop")
        #     time.sleep(1)
    
            #app.mqtt_client.send_message("leds","[1,0,1]")        
            #time.sleep(1)
        #signal.pause() #keeps the program alive but does nothing
    except KeyboardInterrupt:
        print("Goodbye")
        app.robot.drive_system.stop()
        app.mqtt_client.close()


main()

