import gpiozero as gz
import time
import signal


def record_and_light(led_board, color, sequence):
    sequence.append(color)
    function_light(led_board,color, 1)

def function_light(led_board, color, brightness):
    #print("this is a function using the keyword def")
    #rint("It can have many lines")
    if(color == "red"):
        led_board.value = (brightness,0,0)
        time.sleep(0.5)
        led_board.off()
        time.sleep(0.1)
    elif(color == "yellow"):
        led_board.value = (0,brightness,0)
        time.sleep(0.5)
        led_board.off()
        time.sleep(0.1)
    elif(color == "green"):
        led_board.value = (0,0,brightness)
        time.sleep(0.5)
        led_board.off()
        time.sleep(0.1)
def play_sequence(sequence, led_board):
    print(sequence)
    n = len(sequence)
    for i in range(n):
        function_light(led_board, sequence[i], 1)
    sequence.clear()

def button_events():
    print("Button Events")
    button_red = gz.Button(22)
    button_yellow = gz.Button(23)
    button_green = gz.Button(24)
    button = gz.Button(25)
    led_board = gz.LEDBoard(14,15,18,pwm = True)
    sequence = []


    button_red.when_pressed = lambda : record_and_light(led_board,"red", sequence)
    button_yellow.when_pressed = lambda : record_and_light(led_board, "yellow", sequence)
    button_green.when_pressed = lambda : record_and_light(led_board, "green", sequence)
    button.when_pressed = lambda : play_sequence(sequence, led_board)
    signal.pause()




def main():
    print("PushButtons")
    button_events()

main()