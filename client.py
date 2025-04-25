import socket
import threading

class Client:
    def __init__(self, host, port, name=None):
        self.name = name or input("Enter your nickname: ")
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user.connect((host, port))
        self.running = True
        self.callbacks = []  # Callbacks to notify GUI or console

    def add_callback(self, func):
        self.callbacks.append(func)

    def notify(self, message):
        for func in self.callbacks:
            func(message)

    def receive(self):
        while self.running:
            try:
                data = self.user.recv(1024)
                if not data:
                    break
                message = data.decode('ascii')
                if message == 'Name':
                    self.user.send(self.name.encode('ascii'))
                else:
                    self.notify(message)
            except Exception as e:
                self.notify(f"Error: {e}")
                self.running = False
                break

    def send(self, message):
        try:
            self.user.send(message.encode('ascii'))
        except:
            self.notify("Failed to send message.")

    def process_command(self, message):
        command = message.strip().lower()
        if command == 'change':
            new_name = input("Enter your new username: ")
            self.send('change')
            self.send(new_name)
            self.name = new_name
        elif command == 'list':
            self.send('list')
        elif command == 'private':
            recipients = input("Enter recipient names (comma-separated): ")
            private_message = input("Enter your private message: ")
            self.send('private')
            self.send(recipients)
            self.send(private_message)
        elif command == 'exit':
            self.send('exit')
            self.user.close()
            self.running = False
        else:
            self.send(f'{self.name}: {message}')

    def start_console(self):
        threading.Thread(target=self.receive, daemon=True).start()
        while self.running:
            try:
                message = input()
                self.process_command(message)
            except KeyboardInterrupt:
                self.process_command('exit')
                break
