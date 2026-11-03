from rosebot import Rosebot
import time 

def main():
    print("Lab 5b Line Following")
    robot = Rosebot()

    last_turn = "straight"
    try:
        while True:
            print(robot.ultrasonic.get_cm())
            print(robot.line_sensors.get_line_word())
            #Get ultrasonic sensor 

            distance = robot.ultrasonic.get_cm()
            if distance < 20:
                robot.drive_system.stop()
            else:
                word = robot.line_sensors.get_line_word()
                if word == "WBW":
                    robot.drive_system.go(20,20)
                    last_turn = "straight"
                elif word == "BWW" or word == "BBW":
                    robot.drive_system.go(10,40)
                    last_turn = "left"
                elif word == "WWB" or word == "WBB":
                    robot.drive_system.go(-10,-40)
                    last_turn = "right"
                elif word == "WWW":
                    if last_turn == "left":
                        robot.drive_system.go(-10,-40)
                        last_turn = "right"
                    elif last_turn == "straight":
                        robot.drive_system.go(20,20)
                        last_turn = "straight"
                    elif last_turn == "right":
                        robot.drive_system.go(10,40)
                        last_turn = "left"
                elif word == "BBB":
                    robot.drive_system.go(20,20)

            #if distance <20cm
            # stop the robot
            #else
            #get the line sensor readings
            #adjust wheel speeds based on your strategy 

            time.sleep(0.02)
    except KeyboardInterrupt:
        #Handle Ctrl-C to exit the program cleanly.
        robot.drive_system.stop()
        print("Goodbye")
        

main()