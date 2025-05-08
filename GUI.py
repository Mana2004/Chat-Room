import tkinter as tk
from tkinter import Toplevel
from client import Client
import threading

class ChatApp(Client):
    def __init__(self, root, host, port):
        self.root = root
        self.root.title("Chat Room")
        self.root.withdraw()

        # Login window
        self.login_window = Toplevel()
        self.login_window.title("Enter Username")
        self.login_window.geometry("300x150")
        self.login_window.configure(bg="#1e1e1e")

        tk.Label(self.login_window, text="Enter your nickname:", bg="#1e1e1e", fg="white", font=("Consolas", 11)).pack(pady=10)
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(self.login_window, textvariable=self.name_var, bg="#2c2c2c", fg="white", insertbackground="white", font=("Consolas", 11))
        name_entry.pack(pady=5)
        name_entry.focus()

        join_button = tk.Button(self.login_window, text="Join Chat", command=self.get_username, bg="#a591ff", fg="white", font=("Consolas", 10, "bold"), relief=tk.FLAT)
        join_button.pack(pady=10)

        self.login_window.bind("<Return>", lambda event: self.get_username())
        self.root.wait_window(self.login_window)

        # Main chat window
        self.root.deiconify()
        self.root.title("Chat Room")
        self.root.geometry("500x500")
        self.root.configure(bg="#2c2c2c")

        super().__init__(host, port, self.name)

        # Chat display area
        self.chat_frame = tk.Text(self.root, state='disabled', height=20, width=60, wrap='word', bg="#1e1e1e", fg="white", font=("Consolas", 11), bd=0, padx=10, pady=10)
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Entry frame
        self.entry_frame = tk.Frame(self.root, bg="#2c2c2c")
        self.entry_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.entry = tk.Entry(self.entry_frame, width=40, font=("Consolas", 11), bg="#3a3a3a", fg="white", insertbackground="white")
        self.entry.pack(side='left', padx=(0, 10), pady=5, ipady=4, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message, bg="#a591ff", fg="white", activebackground="#4a4aff", font=("Consolas", 10, "bold"), relief=tk.FLAT)
        self.send_button.pack(side='right')

        # Bottom buttons
        self.button_frame = tk.Frame(self.root, bg="#2c2c2c")
        self.button_frame.pack(pady=(0, 10))

        tk.Button(self.button_frame, text="Change Username", command=self.change_username, bg="#444", fg="white", font=("Consolas", 10), relief=tk.FLAT).grid(row=0, column=0, padx=5)
        tk.Button(self.button_frame, text="Private Message", command=self.private_message, bg="#444", fg="white", font=("Consolas", 10), relief=tk.FLAT).grid(row=0, column=1, padx=5)
        tk.Button(self.button_frame, text="List Users", command=self.list_users, bg="#444", fg="white", font=("Consolas", 10), relief=tk.FLAT).grid(row=0, column=2, padx=5)
        tk.Button(self.button_frame, text="Exit", command=self.exit_chat, bg="#ff4d4d", fg="white", font=("Consolas", 10), relief=tk.FLAT).grid(row=0, column=3, padx=5)

        self.chat_frame.tag_configure("user", foreground="white")
        self.chat_frame.tag_configure("[PRIVATE]>", foreground="skyblue")
        self.chat_frame.tag_configure("[SERVER]>", foreground="#a591ff")

        threading.Thread(target=self.receive, args=(self.display_message,), daemon=True).start()

    def get_username(self):
        # Get username and close login window
        self.name = self.name_var.get().strip()
        if self.name:
            self.login_window.destroy()

    def send_message(self):
        # Send message to server
        message = self.entry.get().strip()
        if message:
            if message.lower() == 'exit':
                self.exit_chat()
            else:
                self.send(message)
            self.entry.delete(0, tk.END)

    def exit_chat(self):
        # Exit chat
        self.send("exit")
        self.root.destroy()

    def change_username(self):
        # Change current username
        change_win = Toplevel(self.root)
        change_win.title("Change Username")
        change_win.geometry("300x150")
        change_win.configure(bg="#1e1e1e")

        tk.Label(change_win, text="New username:", bg="#1e1e1e", fg="white", font=("Consolas", 11)).pack(pady=10)
        new_name_var = tk.StringVar()
        tk.Entry(change_win, textvariable=new_name_var, bg="#2c2c2c", fg="white", insertbackground="white", font=("Consolas", 11)).pack(pady=5)

        def confirm():
            new_name = new_name_var.get().strip()
            if new_name:
                self.send("change")
                self.send(new_name)
                change_win.destroy()

        tk.Button(change_win, text="Confirm", command=confirm, bg="#a591ff", fg="white", font=("Consolas", 10, "bold"), relief=tk.FLAT).pack(pady=10)
        change_win.bind("<Return>", lambda event: confirm())

    def private_message(self):
        # Start private message flow
        private_win = Toplevel(self.root)
        private_win.title("Private Message Recipients")
        private_win.geometry("350x150")
        private_win.configure(bg="#1e1e1e")

        tk.Label(private_win, text="Recipients (comma-separated):", bg="#1e1e1e", fg="white", font=("Consolas", 11)).pack(pady=(20, 5))
        recipient_var = tk.StringVar()
        tk.Entry(private_win, textvariable=recipient_var, bg="#2c2c2c", fg="white", insertbackground="white", font=("Consolas", 11)).pack(pady=(0, 10))

        def confirm():
            recipients = recipient_var.get().strip()
            if recipients:
                self.send("private")
                self.send(recipients)
                private_win.destroy()

        tk.Button(private_win, text="Next", command=confirm, bg="#a591ff", fg="white", font=("Consolas", 10, "bold"), relief=tk.FLAT).pack(pady=5)
        private_win.bind("<Return>", lambda event: confirm())

    def list_users(self):
        # Request user list from server
        self.send("list")

    def display_message(self, message):
        # Display incoming message in chat area
        self.chat_frame.config(state='normal')

        if message.startswith('[PRIVATE]>'):
            tag = "[PRIVATE]>"
        elif message.startswith('[SERVER]>'):
            tag = "[SERVER]>"
        else:
            tag = "user"

        self.chat_frame.insert(tk.END, message + "\n", tag)
        self.chat_frame.config(state='disabled')
        self.chat_frame.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root, '127.0.0.1', 15000)
    root.mainloop()
