import socket
import threading

user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user.connect(('127.0.0.1', 15000))

name = input("Enter your nickname: ")

def receive():
    while True:
        try:
            message = user.recv(1024).decode('ascii')
            if message == 'Name':
                user.send(name.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            user.close()
            break

def write():
    global name
    while True:
        message = input("")
        if message.lower() == 'change':
            user.send('change'.encode('ascii'))
            print(user.recv(1024).decode('ascii'))
            name = input("new username: ")
            user.send(name.encode('ascii'))
        elif message.lower() == 'list':
            user.send('list'.encode('ascii'))
            print(user.recv(1024).decode('ascii'))
        elif message.lower() == 'private' :
            user.send('private'.encode('ascii'))
            recipient = input("the recipient names :")
            user.send(recipient.encode('ascii'))
            private_mess = input("your private message:")
            user.send(private_mess.encode('ascii'))
        elif message.lower() == 'exit':
            print("Exiting the chat...")
            user.send('exit'.encode('ascii'))
            user.close()
            break
        else:
            user.send(message.encode('ascii'))



receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

