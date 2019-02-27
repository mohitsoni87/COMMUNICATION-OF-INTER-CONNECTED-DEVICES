import socket
import os
s = socket.socket()
ip, port = '192.168.43.226', 4444
s.connect((ip, port))
name = input('Your Name: ')

print("Welcome to SocketWorld, " + str(name) + "! \n\nHere you can chat with your friends in group and in personal chat as well. You can also share files.\nSome Basics you need to go through.\n\n1. To send message in group, just type your message :)\n2. For Personal Chat, type '@{{ID}} {{message}}'\n3. For file Transfer, type 'FT'\n")
s.send(name.encode())

#Available users
print("Available users: ")


def FileTransfer():
    try:
        while 1:
            filename = input('Filename: ')
            s.send(filename.encode())
            path = input('Path: ')
            s.send(path.encode())
            URL = (s.recv(2048).decode())
            q = os.system('wget ' + str(URL))
            if(q == 0):
                    print("Successfully downloaded!")
                    status = input(("Done? [Y/N]")).upper()            
                    if(status.upper() == "N"):
                        s.send('restart!'.encode())
                        continue
                    else:
                        s.send('done'.encode())
                        break
            else:
                    print("Incorrect details. Please try again!")
                    s.send('restart'.encode())
    except Exception as error:
        print(error)

                    
while(1):
    var = (s.recv(1024).decode('utf-8'))
    #print(var[-1])
    if(var[-1] == "-"):
        if(len(var) != 1):
            print(var[:-1])
        break
        
    else:
        print(str(var))

while(1):

    message = input('Your message: ')
    if(message.lower() == 'ft'):
        s.send('FT'.encode())
        FileTransfer()
    else:
        s.send(message.encode())
        rec = s.recv(1024).decode()
        rec = rec.split('-')
        
        for i in rec:
            if(rec != ''):
                print(i + '\n')
