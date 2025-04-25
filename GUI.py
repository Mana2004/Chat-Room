import tkinter as tk
import threading
from client import Client

class ChatApp:
    def __init__(self, root, host, port):
        self.root = root
        self.root.title("Chat Room")

        name = self.prompt_username()
        self.client = Client(host, port, name)
        self.client.add_callback(self.display_message)

        self.chat_frame = tk.Text(root, state='disabled', height=20, width=50)
        self.chat_frame.pack(pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(side='left', padx=(10, 0))
        self.entry.bind("<Return>", lambda e: self.send())

        self.send_button = tk.Button(root, text="Send", command=self.send)
        self.send_button.pack(side='left', padx=(5, 10))

        threading.Thread(target=self.client.receive, daemon=True).start()

    def prompt_username(self):
        popup = tk.Toplevel()
        popup.title("Enter Username")
        tk.Label(popup, text="Nickname:").pack(pady=5)
        name_var = tk.StringVar()

        entry = tk.Entry(popup, textvariable=name_var)
        entry.pack(pady=5)
        entry.focus()

        def submit():
            popup.destroy()

        tk.Button(popup, text="Join", command=submit).pack(pady=5)
        self.root.wait_window(popup)
        return name_var.get() or "Guest"

    def send(self):
        message = self.entry.get().strip()
        if message:
            self.client.send(f"{self.client.name}: {message}")
            self.entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_frame.config(state='normal')
        self.chat_frame.insert(tk.END, f"{message}\n")
        self.chat_frame.config(state='disabled')
        self.chat_frame.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root, '127.0.0.1', 15000)
    root.mainloop()
