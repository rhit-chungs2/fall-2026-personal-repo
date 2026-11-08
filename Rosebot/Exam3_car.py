import mqtt_helper as mh
import signal
import time
from rosebot import Rosebot


class App:
    def __init__(self):
        self.robot = Rosebot()
        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="ME435/jason/to_pi",
                                 publish_topic_name= "ME435/jason/to_computer")
        self.mqtt_client.callback = self.mqtt_callback

    def mqtt_callback(self, message_type, message_payload):
        print("Recieved type:", message_type)
        print("Recieved payload:", message_payload)
        if message_type == "both":
            print(f"Side: {message_type.capitalize()} Direction: {message_payload[0]} Time: {message_payload[1]} Speed Left: {message_payload[2]} Speed Right: {message_payload[3]}")
        else:
            print(f"Side: {message_type.capitalize()} Direction: {message_payload[0]} Time: {message_payload[1]} Speed: {message_payload[2]}")


  


        if message_type == "left":
            if message_payload[0] == 1:
                self.robot.drive_system.set_speeds(message_payload[2],message_payload[2],0,0)
                time.sleep(message_payload[1])
                self.robot.drive_system.stop()
            else:
                self.robot.drive_system.set_speeds(-message_payload[2],-message_payload[2],0,0)
                time.sleep(message_payload[1])
                self.robot.drive_system.stop()

        if message_type == "right":
            if message_payload[0] == 1:
                self.robot.drive_system.set_speeds(0,0, message_payload[2], message_payload[2])
                time.sleep(message_payload[1])
                self.robot.drive_system.stop()                
            else:
                self.robot.drive_system.set_speeds(0,0, -message_payload[2], -message_payload[2])
                time.sleep(message_payload[1])
                self.robot.drive_system.stop()                
        if message_type == "both":
            if message_payload[0] ==1:
                self.robot.drive_system.set_speeds(message_payload[2],message_payload[2],message_payload[3],message_payload[3])
                time.sleep(message_payload[1])
                self.robot.drive_system.stop()
            else:
                self.robot.drive_system.set_speeds(-message_payload[2],-message_payload[2],-message_payload[3],-message_payload[3])
                time.sleep(message_payload[1])
                self.robot.drive_system.stop()

        # if message_type == "stop":
        #     self.robot.drive_system.set_speeds(0, 0, 0, 0)        
        # if message_type == "beep":
        #     self.robot.buzzer.beep(on_time=0.1, off_time=0.3, n =2)
        
def main():
    print("Exam 3 Car MQTT")
    app = App()
    try:

        while True:
            distance = app.robot.ultrasonic.get_cm()
            print("Ultra: ", distance)
            time.sleep(2)
            app.mqtt_client.send_message("ultra", distance)

        #signal.pause() #keeps the program alive but does nothing
    except KeyboardInterrupt:
        print("Goodbye")
        app.robot.drive_system.stop()
        app.mqtt_client.close()


main()

