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
        
def main():
    print("Car MQTT")

    app = App()
    last_time_sent_s = 0
    try:

         while True:
            right_now = datetime.datetime.now()
            current_time_s = right_now.timestamp()
            print(current_time_s)
            #Strategy is to look at the clock, if two seconds have passed do something.
            if app.is_streaming:
                app.mqtt_client.send_message("Line_sensor_reading",{})

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

