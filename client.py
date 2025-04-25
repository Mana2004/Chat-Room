import socket
import threading

user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user.connect(('127.0.0.1', 15000))

name = input("Enter your nickname: ")

def receive():
    while True:
        try:
            data = user.recv(1024)
            if not data:
                break

            message = data.decode('ascii')
            if message == 'Name':
                user.send(name.encode('ascii'))
            else:
                print(message)

        except OSError:
            break

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


def write():
    global name
    while True:
        message = input()
        cmd = message.lower()

        if cmd == 'change':
            user.send('change'.encode('ascii'))
            new_name = input()
            user.send(new_name.encode('ascii'))
            name = new_name

        elif cmd == 'list':
            user.send('list'.encode('ascii')) 

        elif cmd == 'private':
            user.send('private'.encode('ascii'))
            recipients = input()
            user.send(recipients.encode('ascii'))
            pm = input()
            user.send(pm.encode('ascii'))

        elif cmd == 'exit':
            user.send('exit'.encode('ascii'))
            print("Exiting the chat...")
            user.close()
            break

        else:
            user.send(message.encode('ascii'))

threading.Thread(target=receive).start()
threading.Thread(target=write).start()
