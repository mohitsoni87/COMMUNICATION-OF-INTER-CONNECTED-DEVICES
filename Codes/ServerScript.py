# Python program to implement server side of chat room.
import socket, threading
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('192.168.43.226', 4444))
 
print("Server is Live!")
server.listen(100)
 
list_of_clients = []
l = []

def ClientThread(conn, addr):
    try:
        name = conn.recv(2048).decode('utf-8')
        l.append([conn, name])
        print(l)
        for i in range(len(l)):
            if(l[i][0] != conn):
                print(l[i][1])
                message = str(i) + ' ' + l[i][1]
                conn.send(message.encode())
        conn.send('-'.encode())
    except Exception as error:
        print(error)
        remove(conn)
        
    while True:
        try:
                message = conn.recv(2048).decode()
                if message: 
                    if(message == 'FT'):
                        while(1):
                            try:
                                filename = conn.recv(2048).decode()
                                path = conn.recv(2048).decode()
                                if(path == ''):
                                      dest = filename
                                else:
                                      dest = path + '/' + filename
                                URL = str("http://192.168.43.226:8000/" + dest)
                                conn.send(URL.encode())
                                status = conn.recv(2048).decode('utf-8')
                                if(status == 'restart!'):
                                      continue
                                else:
                                      break
                                conn.send(str.encode(URL))
                            except Exception as error:
                                  print(error, 'FileTransfer')
                                  break
                    elif('@' in message):
                            try:
                                global message_to_send
                                temp = []
                                message = message.split()
                                ID, message_to_send = message[0][1:], '-' + str(l[list_of_clients.index(conn)][1]) + ': ' + message[1]
                                check = 0
                                for t in list_of_clients:
                                    if(check == int(ID)):
                                        temp.append(t)
                                        break
                                    check += 1
                                ToBroadcast = temp
                            except Exception as error:
                                print(error, 'PersonalChat')
                            broadcast(message_to_send, conn, ToBroadcast)
                    else:
                        message_to_send = '-'  + str(l[list_of_clients.index(conn)][1]) + ': ' + message
                        ToBroadcast = list_of_clients
                        broadcast(message_to_send, conn, ToBroadcast)
                else:
                    remove(conn)
        except Exception as error:
            print(error, 'ClientThread')
            remove(conn)
            break

def broadcast(message, connection, ToBroadcast):
    for clients in ToBroadcast: 
        if clients != connection:
            try:
                clients.send(str.encode(message))
            except:
                clients.close()
                # if the link is broken, we remove the client
                remove(clients)

def remove(connection):
    global ind
    if connection in list_of_clients:
        ind = list_of_clients.index(connection)
        l.pop(ind)
        list_of_clients.remove(connection)


 
while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    threading.Thread(target=ClientThread, args=(conn, addr)).start() 
 
conn.close()
server.close()
