import tkinter as tk
from tkinter import simpledialog
from client import Client
import threading

class ChatApp(Client):
    def __init__(self, root, host, port):
        self.root = root
        self.root.title("Chat Room")

        self.root.withdraw()

        name = simpledialog.askstring("Username", "Enter your nickname:", parent=self.root)
        if not name:
            exit()

        self.root.deiconify()

        super().__init__(host, port, name)

        self.chat_frame = tk.Text(root, state='disabled', height=20, width=45, wrap='word')
        self.chat_frame.pack(padx=10, pady=10)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(padx=10, pady=(8, 10), side='left')
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(side='left', padx=(5, 10))

        self.chat_frame.tag_configure("user", foreground="white", background="purple")
        self.chat_frame.tag_configure("private", foreground="white", background="blue")

        threading.Thread(target=self.receive, args=(self.display_message,), daemon=True).start()

    def send_message(self):
        message = self.entry.get().strip()
        if message:
            if message.lower() == 'exit':
                self.exit_chat()
            else:
                self.send(message)
            self.root.after(0, self.entry.delete, 0, tk.END)

    def exit_chat(self):
        self.send("exit")
        self.root.destroy()

    def display_message(self, message):
        self.chat_frame.config(state='normal')

        if message.startswith('Private'):
            self.chat_frame.insert(tk.END, f"{message}\n", "private")
        elif message.startswith('System'):
            self.chat_frame.insert(tk.END, f"{message}\n", "system")
        else:
            self.chat_frame.insert(tk.END, f"{message}\n", "user")

        self.chat_frame.config(state='disabled')
        self.chat_frame.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root, '127.0.0.1', 15000)
    root.mainloop()
