import socket
import threading

host = '127.0.0.1' #192.168.87.138
port = 15000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

users = []
names = []

def show(message):
    for user in users:
        try:
            user.send(message)
        except:
            users.remove(user)

def manage(user):
    while True:
        try:
            message = user.recv(1024).decode('ascii')
            if message.lower() == 'change':
                user.send('new username:'.encode('ascii'))
                new_name = user.recv(1024).decode('ascii')
                index = users.index(user)
                old_name = names[index]
                names[index] = new_name
                show(f'{old_name} changed their username to {new_name}'.encode('ascii'))

            elif message.lower() == 'list':
                user_list = ', '.join(names)
                user.send(f'Users in the chatroom: {user_list}'.encode('ascii'))

            elif message.lower() == 'private':
                user.send('the recipient names (comma-separated): '.encode('ascii'))
                recipients = user.recv(1024).decode('ascii').split(',')
                recipients = [r.strip() for r in recipients]

                valid = []
                invalid = []
                for recipient in recipients:
                    if recipient in names:
                        valid.append(recipient)
                    else:
                        invalid.append(recipient)

                if invalid:
                    user.send(f'user(s) not found: {", ".join(invalid)}'.encode('ascii'))
                if valid:
                    user.send('your private message:'.encode('ascii'))
                    private_message = user.recv(1024).decode('ascii')

                    for recipient in valid:
                        index = names.index(recipient)
                        recipient_user = users[index]
                        recipient_user.send(
                            f'private message from {names[users.index(user)]}: {private_message}'.encode('ascii'))

                    user.send(f'Private message sent to: {", ".join(valid)}'.encode('ascii'))

            elif message.lower() == 'exit':
                raise Exception("Client requested disconnect.")

            else:
                index = users.index(user)
                name = names[index]
                public_message = f'{name}: {message}'
                show(public_message.encode('ascii'))

        except Exception as e:
            if user in users:
                index = users.index(user)
                name = names[index]
                users.remove(user)
                names.remove(name)
                show(f'{name} left the chat.'.encode('ascii'))
            user.close()
            break

def receive():
    while True:
        user, address = server.accept()
        print(f"connected with {address}")

        user.send('Name'.encode('ascii'))
        name = user.recv(1024).decode('ascii')
        names.append(name)
        users.append(user)

        print(f'name of the user is {name}')
        show(f'{name} joined the chat'. encode('ascii'))
        user.send('connected to the server'.encode('ascii'))

        thread = threading.Thread(target=manage, args=(user,))
        thread.start()

print("server is listening...")
receive()

