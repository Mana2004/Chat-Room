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
                user.send('the recipinet name: '.encode('ascii'))
                recipient = user.recv(1024).decode('ascii')
                if recipient in names:
                    index = names.index(recipient)
                    recipient_user = users[index]
                    user.send('your private message:'.encode('ascii'))
                    private_message = user.recv(1024).decode('ascii')
                    recipient_user.send(f'private message from {names[users.index(user)]}')
                    recipient_user.send(private_message.encode('ascii'))
                else:
                    user.send('user not found'.encode('ascii'))
            else:
                index = users.index(user)
                name = names[index]
                public_message = f'{name}: {message}'
                show(public_message.encode('ascii'))
        except:
            index = users.index(user)
            users.remove(user)
            user.close()
            name = names[index]
            names.remove(name)
            show(f'{name} left the chat.'.encode('ascii'))
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

