import tkinter as tk
import socket
import threading

# Dirección del servidor (tu IP local)
server_address = ('192.168.1.82', 12345)

# Función para recibir mensajes del servidor
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                display_message(message)
        except:
            break

# Función para mostrar el mensaje en la interfaz
def display_message(message):
    chat_text.config(state=tk.NORMAL)  # Habilitar la edición para insertar el mensaje
    chat_text.insert(tk.END, message + '\n')
    chat_text.yview(tk.END)  # Desplazar hacia abajo
    chat_text.config(state=tk.DISABLED)  # Deshabilitar la edición

# Función para enviar el mensaje al servidor y mostrarlo en la interfaz
def send_message(event=None):
    message = message_entry.get()
    if message:
        # Mostrar el mensaje del usuario en su ventana
        display_message(f"{username}: {message}")
        
        # Enviar el mensaje al servidor
        client_socket.send(message.encode('utf-8'))
        
        # Limpiar la entrada del mensaje
        message_entry.delete(0, tk.END)

# Función para iniciar la aplicación y conectar al servidor
def start_chat():
    global client_socket, username
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    # Pedimos el nombre
    username = name_entry.get()
    client_socket.send(username.encode('utf-8'))
    
    # Crear un hilo para recibir mensajes
    threading.Thread(target=receive_messages, daemon=True).start()

    start_window.withdraw()  # Ocultar la ventana de inicio
    chat_window.deiconify()  # Mostrar la ventana de chat

# Ventana de chat
chat_window = tk.Tk()
chat_window.title("R3Chat")
chat_window.geometry("500x600")
chat_window.configure(bg="#2E2E2E")

chat_text = tk.Text(chat_window, state=tk.DISABLED, bg="#2E2E2E", fg="white", font=("Arial", 12))
chat_text.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

message_entry = tk.Entry(chat_window, font=("Arial", 14))
message_entry.pack(pady=10, padx=10, fill=tk.X)
message_entry.bind("<Return>", send_message)

# Ventana inicial para pedir el nombre
start_window = tk.Tk()
start_window.title("Bienvenido a R3Chat")
start_window.geometry("300x200")

name_label = tk.Label(start_window, text="Introduce tu nombre:", font=("Arial", 12))
name_label.pack(pady=10)

name_entry = tk.Entry(start_window, font=("Arial", 14))
name_entry.pack(pady=10)

start_button = tk.Button(start_window, text="Comenzar", font=("Arial", 12), command=start_chat)
start_button.pack(pady=10)

start_window.mainloop()
