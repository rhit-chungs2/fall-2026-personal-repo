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
            response = loader.send_command("RESET")
            print(response)



    loader.disconnect()
    print("Goodbye")



main()