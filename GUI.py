import tkinter as tk
from client import Client

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")
        self.client = Client()
        
        self.chat_frame = tk.Text(root, state='disabled', height=20, width=50)
        self.chat_frame.pack(pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(side='left', padx=(10, 0))
        self.entry.bind("<Return>", lambda e: self.send())

        self.send_button = tk.Button(root, text="Send", command=self.send)
        self.send_button.pack(side='left', padx=(5, 10))

        self.ask_username()

    def ask_username(self):
        def on_submit():
            name = name_entry.get().strip()
            if name:
                self.client.start(name, self.display_message)
                popup.destroy()
        popup = tk.Toplevel(self.root)
        popup.title("Enter Username")
        tk.Label(popup, text="Enter your nickname:").pack(padx=10, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack(padx=10)
        name_entry.focus()
        tk.Button(popup, text="Join", command=on_submit).pack(pady=5)

    def send(self):
        msg = self.entry.get().strip()
        if msg:
            self.client.send(msg)
            self.entry.delete(0, tk.END)

    def display_message(self, msg):
        self.chat_frame.config(state='normal')
        self.chat_frame.insert(tk.END, msg + '\n')
        self.chat_frame.config(state='disabled')
        self.chat_frame.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
