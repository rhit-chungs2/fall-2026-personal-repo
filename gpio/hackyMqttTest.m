function hackyMqttTest()
clc
fprintf("Hacky MQTT Test in MATLAB\n")
mqClient = mqttclient("tcp://mosquitto.csse.rose-hulman.edu");


mqClient.Connected

end
