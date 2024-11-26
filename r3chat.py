import socket
import threading
import tkinter as tk
from tkinter import simpledialog

# Configuración del cliente
SERVER = '192.168.1.82'  # Dirección IP del servidor
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
def connect_to_server():
    client.connect((SERVER, PORT))
    username = simpledialog.askstring("Nombre", "Ingresa tu nombre:")
    client.send(username.encode())

# Recibir mensajes del servidor
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat_box.insert(tk.END, message + "\n")
        except:
            break

# Enviar mensaje al servidor
def send_message(event=None):
    message = message_entry.get()
    if message:
        client.send(message.encode())
        message_entry.delete(0, tk.END)

# Crear la interfaz de usuario
def create_gui():
    global chat_box, message_entry
    
    window = tk.Tk()
    window.title("Chat R3Chat")

    chat_box = tk.Text(window, height=20, width=50, state=tk.DISABLED)
    chat_box.pack()

    message_entry = tk.Entry(window, width=50)
    message_entry.bind("<Return>", send_message)
    message_entry.pack()

    send_button = tk.Button(window, text="Enviar", command=send_message)
    send_button.pack()

    window.protocol("WM_DELETE_WINDOW", window.quit)
    window.mainloop()

# Iniciar la conexión y la interfaz gráfica
def start_client():
    connect_to_server()
    threading.Thread(target=receive_messages, daemon=True).start()
    create_gui()

if __name__ == '__main__':
    start_client()
