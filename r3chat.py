import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '192.168.1.82'
PORT = 12345
ROLE_ADMIN_IP = '192.168.1.82'

role = "Usuario"

def display_message(message, is_sent=True):
    chat_area.config(state=tk.NORMAL)
    if is_sent:
        chat_area.insert(tk.END, f"Tú: {message}\n", "sent")
    else:
        chat_area.insert(tk.END, f"Usuario: {message}\n", "received")
    chat_area.yview(tk.END)
    chat_area.config(state=tk.DISABLED)

def receive_messages():
    global connected
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                display_message(message, is_sent=False)
            else:
                connected = False
                break
        except:
            messagebox.showerror("Error", "Conexión perdida con el servidor.")
            break

def send_message(event=None):
    message = message_input.get()
    if message.strip():
        if message.startswith("/clear"):
            chat_area.config(state=tk.NORMAL)
            chat_area.delete(1.0, tk.END)
            chat_area.config(state=tk.DISABLED)
        else:
            display_message(message, is_sent=True)
            client_socket.send(message.encode())
        message_input.delete(0, tk.END)

def toggle_role():
    global role
    if role == "Usuario" and client_socket.getpeername()[0] == ROLE_ADMIN_IP:
        role = "Admin"
        role_label.config(text=f"Rol: {role}")
    else:
        messagebox.showerror("Error", "Solo el servidor puede ser administrador")

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    connected = True

    if client_socket.getpeername()[0] == ROLE_ADMIN_IP:
        role = "Admin"
except Exception as e:
    messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
    exit()

root = tk.Tk()
root.title("R3 Chat")

device_name = socket.gethostname()

root.geometry("500x400")
root.configure(bg="#2c3e50")

title_label = tk.Label(root, text="R3 Chat", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#34495e")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=15, state=tk.DISABLED, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 10))
chat_area.pack(pady=5)

message_input = tk.Entry(frame, width=40, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 10))
message_input.pack(side=tk.LEFT, padx=(0, 10), pady=(0, 10))

send_button = tk.Button(frame, text="Enviar", command=send_message, bg="#1abc9c", fg="#ffffff", font=("Helvetica", 10, "bold"))
send_button.pack(side=tk.LEFT, pady=(0, 10))

role_button = tk.Button(frame, text="Cambiar a Admin", command=toggle_role, bg="#f39c12", fg="#ffffff", font=("Helvetica", 10, "bold"))
role_button.pack(side=tk.LEFT, pady=(0, 10))

role_label = tk.Label(frame, text=f"Rol: {role}", bg="#34495e", fg="#ecf0f1", font=("Helvetica", 10))
role_label.pack(side=tk.LEFT, padx=(10, 0))

message_input.bind('<Return>', send_message)

threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()

# Coded by R3-K1