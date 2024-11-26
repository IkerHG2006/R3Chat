import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '192.168.1.82'
PORT = 12345

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_area.config(state=tk.NORMAL)
            chat_area.insert(tk.END, message + '\n')
            chat_area.yview(tk.END)
            chat_area.config(state=tk.DISABLED)
        except:
            messagebox.showerror("Error", "Conexión perdida con el servidor.")
            break

def send_message(event=None):
    message = message_input.get()
    if message.strip():
        formatted_message = f"{device_name}: {message}"
        client_socket.send(formatted_message.encode('utf-8'))
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Tú: " + message + '\n')
        chat_area.yview(tk.END)
        chat_area.config(state=tk.DISABLED)
        message_input.delete(0, tk.END)

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
except Exception as e:
    messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
    exit()

root = tk.Tk()
root.title("R3 Chat")

device_name = socket.gethostname()

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
chat_area.pack()

message_input = tk.Entry(frame, width=40)
message_input.pack(side=tk.LEFT, padx=(0, 10))

send_button = tk.Button(frame, text="Enviar", command=send_message)
send_button.pack(side=tk.LEFT)

message_input.bind('<Return>', send_message)

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()

# Coded by R3-K1