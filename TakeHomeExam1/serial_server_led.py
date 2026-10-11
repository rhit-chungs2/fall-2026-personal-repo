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

@app.get("/api/<command>")
def handle_plateloader_commands(command):
    with serial_lock:
        response = led.send_command(command)
    return response




if __name__ == "__main__":
    print("Running flask!")
    led.connect() 

    try: 
        app.run(host = "0.0.0.0",port = 8080, debug=True)
    finally:
        print("Disconnecting plate loader")
        led.disconnect()
