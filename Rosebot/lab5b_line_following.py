from rosebot import Rosebot
import time 

def main():
    print("Lab 5b Line Following")
    robot = Rosebot()


    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        #Handle Ctrl-C to exit the program cleanly.
        robot.drive_system.stop()
        print("Goodbye")
        

main()