import socket
import threading


class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        print(f"Server started on {host}:{port}")

        self.users = []
        self.names = []

    def broadcast(self, message):
        """Sends a message to all connected users."""
        for user in self.users:
            try:
                user.send(message)
            except:
                self.remove_user(user)

    def remove_user(self, user):
        """Removes a user from the chat."""
        if user in self.users:
            index = self.users.index(user)
            name = self.names[index]
            self.users.remove(user)
            self.names.remove(name)
            user.close()
            self.broadcast(f'{name} left the chat.'.encode('ascii'))

    def handle_user(self, user):
        while True:
            try:
                message = user.recv(1024).decode('ascii')
                if message.lower() == 'change':
                    user.send('Enter your new username:'.encode('ascii'))
                    new_name = user.recv(1024).decode('ascii')
                    index = self.users.index(user)
                    old_name = self.names[index]
                    self.names[index] = new_name
                    self.broadcast(f'{old_name} changed their username to {new_name}'.encode('ascii'))
                elif message.lower() == 'list':
                    user_list = ', '.join(self.names)
                    user.send(f'Users in the chatroom: {user_list}'.encode('ascii'))
                elif message.lower() == 'private':
                    user.send('Enter recipient names (comma-separated): '.encode('ascii'))
                    recipients = user.recv(1024).decode('ascii').split(',')
                    recipients = [r.strip() for r in recipients]

                    valid = []
                    invalid = []
                    for recipient in recipients:
                        if recipient in self.names:
                            valid.append(recipient)
                        else:
                            invalid.append(recipient)

                    if invalid:
                        user.send(f'User(s) not found: {", ".join(invalid)}'.encode('ascii'))
                    if valid:
                        user.send('Enter your private message: '.encode('ascii'))
                        private_message = user.recv(1024).decode('ascii')
                        for recipient in valid:
                            index = self.names.index(recipient)
                            recipient_user = self.users[index]
                            recipient_user.send(f'Private message from {self.names[self.users.index(user)]}: {private_message}'.encode('ascii'))
                        user.send(f'Private message sent to: {", ".join(valid)}'.encode('ascii'))
                elif message.lower() == 'exit':
                    raise Exception("Client requested disconnect.")
                else:
                    index = self.users.index(user)
                    name = self.names[index]
                    public_message = f'{name}: {message}'
                    self.broadcast(public_message.encode('ascii'))
            except:
                self.remove_user(user)
                break

    def start(self):
        while True:
            user, address = self.server.accept()
            print(f"Connected with {address}")

            user.send('Name'.encode('ascii'))
            name = user.recv(1024).decode('ascii')
            self.users.append(user)
            self.names.append(name)

            print(f"Name of the client is {name}")
            self.broadcast(f'{name} joined the chat.'.encode('ascii'))
            user.send('Connected to the server.'.encode('ascii'))

            thread = threading.Thread(target=self.handle_user, args=(user,))
            thread.start()


if __name__ == "__main__":
    server = Server('0.0.0.0', 15000)
    server.start()

