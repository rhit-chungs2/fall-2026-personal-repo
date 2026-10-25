from gpiozero import LED
from time import sleep

red = LED(14)
green = LED(15)
blue = LED(18)

red.blink()
green.blink()
blue.blink()

sleep(10)        # let them blink for a while

red.close()      # stops each blink thread cleanly
green.close()
blue.close()