import flask 

app = flask.Flask(__name__)



@app.get("/api/Hello/<name>")
def hello_name(name):
    return f"Good {name}!"

@app.get('/')
def handle_haked_domain():
    return flask.redirect("/api/Hello/Test")    





if __name__ == "__main__":
    print("Running flask!") 
    app.run(host = "0.0.0.0",port = 8080, debug=True)