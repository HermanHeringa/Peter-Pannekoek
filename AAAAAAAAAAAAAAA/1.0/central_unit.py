import socket
import keyboard




def start():
    #Define buffer for messages
    messages = []
    #Counter for last message that is read
    last_message = 0
    

    while True:

        #If the buffer is empty read any incoming messages
        if len(messages) <= last_message:
            with open("Messages.txt", 'r') as f:
                messages = f.readlines()

                
        #If there are any messages in the buffer that have not been read
        if len(messages) > last_message:
            #Print out new message
            print(messages[last_message])
            #Increment which message has been read last
            last_message += 1

        #When program is terminated delete everything in the file
        #And then close it
        if keyboard.is_pressed('SPACE'):
            file = open("Messages.txt", 'w')
            file.truncate()
            file.close()
            break
print("[STARTING] Central Unit")
print("[INFO] To terminate press SPACEBAR")
start()