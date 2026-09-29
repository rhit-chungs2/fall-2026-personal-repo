import plateloader 

def main():
    loader = plateloader.PlateLoader()
    loader.connect()
    #loader = plateloader.PlateLoader("/dev/ttyUSB0")

    while True:
        print ("           ")
        print ("Serial Menu")
        print ("0. Exit")
        print ("1. RESET")
        print ("2. X-AXIS")
        print ("3. GRIPPER")
        print ("4. Z-AXIS")
        print ("5. Move")
        print ("6. Status")
        selection = int(input("Selection: "))
        if selection == 0:
            break
        elif selection ==1:
            loader.send_command("RESET")
            #response = loader.send_command("RESET")
            #print(response)
        elif selection ==2:
            xaxis = int(input("X-Axis to:"))
            loader.send_command(f"X-AXIS {xaxis}")
        elif selection == 3:
            gripper = input("GRIPPER OPEN or CLOSE:")
            if gripper == "OPEN":
                loader.send_command("GRIPPER OPEN")
            elif gripper == "CLOSE":
                loader.send_command("GRIPPER CLOSE")
        elif selection == 4:
            zaxis = input("Select EXTEND or RETRACT:")
            if zaxis == "EXTEND":
                loader.send_command("Z-AXIS EXTEND")
            elif zaxis == "RETRACT":
                loader.send_command("Z-AXIS RETRACT")
        elif selection ==5:
            movefrom = int(input("From:"))
            moveto = int(input("To:"))
            loader.send_command(f"MOVE {movefrom} {moveto}")
        elif selection ==6:
            loader.send_command("LOADER_STATUS")
    loader.disconnect()
    print("Goodbye")



main()