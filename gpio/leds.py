import gpiozero as gz
import time
import signal


def basic_on_off():
    print("Basic On / Off")
    green_led = gz.DigitalOutputDevice(18)
    green_led.on()
    time.sleep(5)
    green_led.off()

def fancy_leds():
    print("Fancy LEDs")
    red_led = gz.LED(14)
    yellow_led = gz.LED(15)
    green_led = gz.LED(18)

    #yellow_led.blink(on_time = 2, off_time = 0.1, n = 3 , background= False)
    #yellow_led.blink(on_time = 2, off_time = 0.1)
    #signal.pause()

    red_led.blink(on_time=2, off_time = 0.1)
    time.sleep(0.1)
    yellow_led.blink(on_time=2, off_time = 0.1)
    time.sleep(0.1)
    green_led.blink(on_time=2, off_time = 0.1)

def led_board():
    print("LED Board")
    red_led = gz.DigitalOutputDevice(14)
    yellow_led = gz.DigitalOutputDevice(15)
    green_led = gz.DigitalOutputDevice(18)

    # TODO: Figure out how to use an LEDBoard for pins 14, 15, 18
    led_board = gz.LEDBoard(14,15,18,pwm=True)
    for i in range(5):
        #led_board.on()
        red_led.on()
        yellow_led.on()
        green_led.on()
        time.sleep(1)

        #led_board.off()
        red_led.off()
        yellow_led.off()
        green_led.off()
        time.sleep(1)

        #led_board.value(1,0,1)
        red_led.on()
        green_led.on()
        time.sleep(1)

        led_board.value =(0,0.5,0)
        time.sleep(1)
    # Construct it
    # Make a loop that runs 5 times.
    # Turn on all the LEDs
    # Wait 1 second
    # Turn off all the LEDs
    # Wait 1 second
    # turn on just Red and Green
    # Wait 1 second

    # Turn on just yellow at 0.5 brightness
    # Wait 1 second

def main():
    print("Leds")
    #basic_on_off()
    #fancy_leds()
    led_board()


main()
