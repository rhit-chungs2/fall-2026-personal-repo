import gpiozero as gz
import time
import signal

def button_state():
    print("Button State")
    button = gz.Button(25)

    while True:
        if button.is_pressed:
            print("Button is pressed")
        else:
            print("Button is Not pressed")
        time.sleep(0.1)

def function_using_def():
    print("this is a function using the keyword def")
    print("It can have many lines")

function_using_lambda = lambda: print("This is a func object using the keyword lambda")


def some_helper_function(led_board, brightness):
    print("some helper function")  
    led_board.value = (brightness,0,brightness)
    time.sleep(1)
    led_board.off()
    time.sleep(1)
def button_events():
    print("Button Events")
    button = gz.Button(25)
    led_board = gz.LEDBoard(14,15,18,pwm = True)
    button.when_pressed = function_using_def
    button.when_released = function_using_lambda
    button.when_held = lambda : some_helper_function(led_board, 0.3)
    signal.pause()




def main():
    print("PushButtons")
    #button_state()
    button_events()

main()