import socket
import threading

class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        print(f"Server is listening on {host}:{port}")

        self.users = []
        self.names = []

    def broadcast(self, message):
        for user in self.users:
            try:
                user.send(message)
            except:
                self.remove_user(user)

    def remove_user(self, user):
        if user in self.users:
            index = self.users.index(user)
            name = self.names[index]
            self.users.remove(user)
            self.names.remove(name)
            user.close()
            self.broadcast(f'[SERVER]> {name} left the chat.'.encode('ascii'))

    def handle_user(self, user):
        try:
            name = user.recv(1024).decode('ascii')
            self.users.append(user)
            self.names.append(name)
            self.broadcast(f'[SERVER]> {name} joined the chat.'.encode('ascii'))

            while True:
                message = user.recv(1024).decode('ascii')
                if message.lower() == 'change':
                    user.send('[SERVER]> Enter your new username:'.encode('ascii'))
                    new_name = user.recv(1024).decode('ascii')
                    index = self.users.index(user)
                    old_name = self.names[index]
                    self.names[index] = new_name
                    self.broadcast(f'[SERVER]> {old_name} changed their username to {new_name}'.encode('ascii'))
                    name = new_name

                elif message.lower() == 'list':
                    user_list = ', '.join(self.names)
                    user.send(f'[SERVER]> Users in the chatroom: {user_list}'.encode('ascii'))

                elif message.lower() == 'private':
                    user.send('[SERVER]> Enter recipient names (comma-separated): '.encode('ascii'))
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
                        user.send(f'[SERVER]> User(s) not found: {", ".join(invalid)}'.encode('ascii'))

                    if valid:
                        user.send('[SERVER]> Enter your private message: '.encode('ascii'))
                        private_message = user.recv(1024).decode('ascii')
                        for recipient in valid:
                            idx = self.names.index(recipient)
                            recipient_user = self.users[idx]
                            recipient_user.send(f'[PRIVATE]> Private message from {name}: {private_message}'.encode('ascii'))
                        user.send(f'[PRIVATE]> Private message sent to: {", ".join(valid)}'.encode('ascii'))

                elif message.lower() == 'exit':
                    raise Exception("[SERVER]> Client requested disconnect.")

                else:
                    self.broadcast(f'{name}: {message}'.encode('ascii'))

        except:
            self.remove_user(user)

    def start(self):
        while True:
            user, address = self.server.accept()
            print(f"Connected with {address}")
            thread = threading.Thread(target=self.handle_user, args=(user,))
            thread.start()

if __name__ == "__main__":
    server = Server('0.0.0.0', 15000)
    server.start()