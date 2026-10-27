import mqtt_helper as mh
import time

def mqtt_callback(message_type , message_payload):
    print("The message type is ", message_type)
    print("The message payload is ", message_payload)



def main():
    print("Hacky MQTT test")
    mqtt_client = mh.MqttClient()
    mqtt_client.connect(subscription_topic_name="woot/#",
                        publish_topic_name="woot/sending",
                        use_off_campus_broker=False)
    mqtt_client.callback = mqtt_callback


    counter = 0 
    while True:
        mqtt_client.send_message("hello", counter)
        time.sleep(0.1)
        counter += 1


    




main()