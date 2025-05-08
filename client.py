import socket

class Client:
    def __init__(self, host, port, name):
        # Initialize and connect socket to the server
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user.connect((host, port))
        self.name = name
        self.running = True
        # Send the username to the server
        self.user.send(self.name.encode('ascii'))

    def send(self, message):
        # Send a message to the server
        try:
            self.user.send(message.encode('ascii'))
        except:
            print("Failed to send message.")

    def receive(self, callback):
        # Listen for messages and pass them to a callback
        while self.running:
            try:
                message = self.user.recv(1024).decode('ascii')
                callback(message)
            except:
                print("Disconnected from the server.")
                self.running = False
                break
