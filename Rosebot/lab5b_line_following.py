from rosebot import Rosebot
import time 

def main():
    print("Lab 5b Line Following")
    robot = Rosebot()


    try:
        while True:


            print(robot.ultrasonic.get_cm())
            print(robot.line_sensors.get_line_word())
            #Get ultrasonic sensor 
            #if distance <20cm
            # stop the robot
            #else

            #get the line sensor readings
            #adjust wheel speeds based on your strategy 

            time.sleep(0.1)
    except KeyboardInterrupt:
        #Handle Ctrl-C to exit the program cleanly.
        robot.drive_system.stop()
        print("Goodbye")
        

main()