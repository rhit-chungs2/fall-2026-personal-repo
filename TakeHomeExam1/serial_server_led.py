import flask 
import led
import threading


app = flask.Flask(__name__,static_url_path="",static_folder="public")


serial_lock = threading.Lock()
led = led.LED() #TODO: set the port if needed.
#loader = plateloader.PlateLoader("/dev/ttyUSB0") #TODO: set the port if needed.




@app.route('/')
def handle_haked_domain():
    #return flask.redirect("/prettyone.html")  
    return flask.redirect("/led.html")   
 
@app.get("/api/<command>/<parameter>")
def handle_led_commands(command,parameter):
    if command == "led":
        if parameter == "on":
            send = "LED ON"
            response =led.send_command(send)
            return response
        elif parameter == "off":
            send = "LED OFF"
            response = led.send_command(send)
            return response

@app.get("/api/<command>/<parameter1>/<parameter2>")
def handle_flash_commands(command,parameter1,parameter2):
    if command == "flash":
            send = "FLASH" + str(parameter1) + " " + str(parameter2)
            response =led.send_command(send)
            return response




if __name__ == "__main__":
    print("Running flask!")
    led.connect() 

    try: 
        app.run(host = "0.0.0.0",port = 8080, debug=True)
    finally:
        print("Disconnecting LED goodbye")
        led.disconnect()
