import socket
import threading

class Server:
    def __init__(self, host, port):
        # Create a TCP/IP socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the specified host and port
        self.server.bind((host, port))
        # Listen for incoming connections
        self.server.listen()
        print(f"Server is listening on {host}:{port}")

        # Lists to keep track of connected clients and their usernames
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
            # Remove user and name from tracking lists
            self.users.remove(user)
            self.names.remove(name)
            user.close()
            # Notify remaining clients
            self.broadcast(f'[SERVER]> {name} left the chat.'.encode('ascii'))

    def handle_user(self, user):
        try:
            # First message from client is their username
            name = user.recv(1024).decode('ascii')
            self.users.append(user)
            self.names.append(name)
            # Notify all clients about the new connection
            self.broadcast(f'[SERVER]> {name} joined the chat.'.encode('ascii'))
            # Send a welcome message to the new client
            user.send(f'\n[SERVER]> Hello {name}'.encode('ascii'))

            while True:
                # Receive a message from the client
                message = user.recv(1024).decode('ascii')

                # Change username command
                if message.lower() == 'change':
                    user.send('[SERVER]> Enter your new username:'.encode('ascii'))
                    new_name = user.recv(1024).decode('ascii')
                    index = self.users.index(user)
                    old_name = self.names[index]
                    self.names[index] = new_name
                    # Broadcast name change event
                    self.broadcast(f'[SERVER]> {old_name} changed their username to {new_name}'.encode('ascii'))
                    name = new_name

                # List users command
                elif message.lower() == 'list':
                    user_list = ', '.join(self.names)
                    user.send(f'[SERVER]> Users in the chatroom: {user_list}'.encode('ascii'))

                # Private messaging flow
                elif message.lower() == 'private':
                    # Ask for recipient names
                    user.send('[SERVER]> Enter recipient names (comma-separated): '.encode('ascii'))
                    recipients = user.recv(1024).decode('ascii').split(',')
                    recipients = [r.strip() for r in recipients]

                    valid = []  # valid recipients
                    invalid = []  # not found usernames
                    for recipient in recipients:
                        if recipient in self.names:
                            valid.append(recipient)
                        else:
                            invalid.append(recipient)

                    # Notify if any invalid users
                    if invalid:
                        user.send(f'[SERVER]> User(s) not found: {", ".join(invalid)}'.encode('ascii'))

                    # If valid recipients exist, ask for the private message
                    if valid:
                        user.send('[SERVER]> Enter your private message: '.encode('ascii'))
                        private_message = user.recv(1024).decode('ascii')
                        # Send private message to each valid recipient
                        for recipient in valid:
                            idx = self.names.index(recipient)
                            recipient_user = self.users[idx]
                            recipient_user.send(f'[PRIVATE]> Private message from {name}: {private_message}'.encode('ascii'))
                        # Confirm to sender
                        user.send(f'[PRIVATE]> Private message sent to: {", ".join(valid)}'.encode('ascii'))

                # Exit command: raise exception to break loop and cleanup
                elif message.lower() == 'exit':
                    raise Exception("[SERVER]> Client requested disconnect.")

                # Standard broadcast for normal messages
                else:
                    self.broadcast(f'{name}: {message}'.encode('ascii'))

        except:
            # Cleanup on any error or disconnect
            self.remove_user(user)

    def start(self):
        while True:
            user, address = self.server.accept()
            print(f"Connected with {address}")
            thread = threading.Thread(target=self.handle_user, args=(user,))
            thread.start()

if __name__ == "__main__":
    # Start the server on all interfaces, port 15000
    server = Server('0.0.0.0', 15000)
    server.start()
