import socket
import threading

class Client:
    def __init__(self, host, port):
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user.connect((host, port)) #192.168.87.138
        self.name = input("Enter your nickname: ")

    def receive(self):
        while True:
            try:
                data = self.user.recv(1024)
                if not data:
                    break

                message = data.decode('ascii')
                if message == 'Name':
                    self.user.send(self.name.encode('ascii'))
                else:
                    print(f'\n{message}')
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                self.user.close()
                break

    def write(self):
        while True:
            message = input()
            command = message.lower()

            if command == 'change':
                self.user.send('change'.encode('ascii'))
                new_name = input("Enter your new username: ")
                self.user.send(new_name.encode('ascii'))
                self.name = new_name
            elif command == 'list':
                self.user.send('list'.encode('ascii'))
            elif command == 'private':
                self.user.send('private'.encode('ascii'))
                recipients = input("Enter recipient names (comma-separated): ")
                self.user.send(recipients.encode('ascii'))
                private_message = input("Enter your private message: ")
                self.user.send(private_message.encode('ascii'))
            elif command == 'exit': 
                print("Exiting the chat...")
                self.user.send('exit'.encode('ascii'))
                self.user.close()
                break
            else:
                self.user.send(f'{self.name}: {message}'.encode('ascii'))

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__ == "__main__":
    client = Client('127.0.0.1', 15000)
    client.start()