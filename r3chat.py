import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configuración de colores personalizables
class Theme:
    DARK = {
        "bg": "black",           # Fondo oscuro
        "fg": "white",           # Texto blanco
        "btn_bg": "#4CAF50",     # Botón verde
        "btn_fg": "white",       # Texto botón blanco
        "entry_bg": "#2a2a2a",   # Fondo entrada texto oscuro
        "entry_fg": "white",     # Texto entrada blanco
        "title": "Chat Oscuro"
    }
    
    LIGHT = {
        "bg": "white",           # Fondo claro
        "fg": "black",           # Texto negro
        "btn_bg": "#008CBA",     # Botón azul
        "btn_fg": "white",       # Texto botón blanco
        "entry_bg": "#f1f1f1",   # Fondo entrada texto claro
        "entry_fg": "black",     # Texto entrada negro
        "title": "Chat Claro"
    }

# Selección de tema (puedes cambiar a LIGHT para un tema claro)
THEME = Theme.DARK

# Conectar al servidor
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.82', 12345))  # IP del servidor
    return client_socket

# Función para recibir mensajes
def receive_messages(client_socket, chat_box):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_box.insert(tk.END, f"{message}\n")
                chat_box.yview(tk.END)
        except:
            break

# Función para enviar mensajes
def send_message(client_socket, entry_field):
    message = entry_field.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        entry_field.delete(0, tk.END)

# Función para manejar la tecla Enter
def on_enter(client_socket, entry_field):
    send_message(client_socket, entry_field)

# Función para crear la interfaz gráfica
def create_gui(client_socket):
    # Crear ventana principal
    window = tk.Tk()
    window.title(THEME["title"])

    # Configurar colores de fondo y fuente
    window.configure(bg=THEME["bg"])

    # Crear cuadro de texto para mostrar los mensajes
    chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20, 
                                         bg=THEME["bg"], fg=THEME["fg"], font=("Arial", 12))
    chat_box.grid(row=0, column=0, padx=10, pady=10)

    # Crear campo de entrada para escribir mensajes
    entry_field = tk.Entry(window, width=40, font=("Arial", 12), 
                           bg=THEME["entry_bg"], fg=THEME["entry_fg"])
    entry_field.grid(row=1, column=0, padx=10, pady=10)

    # Crear botón para enviar el mensaje
    send_button = tk.Button(window, text="Enviar", command=lambda: send_message(client_socket, entry_field),
                            bg=THEME["btn_bg"], fg=THEME["btn_fg"], font=("Arial", 12))
    send_button.grid(row=2, column=0, pady=10)

    # Configurar el evento de Enter para enviar el mensaje
    entry_field.bind("<Return>", lambda event: on_enter(client_socket, entry_field))

    # Iniciar hilo para recibir mensajes
    threading.Thread(target=receive_messages, args=(client_socket, chat_box), daemon=True).start()

    # Ejecutar la interfaz gráfica
    window.mainloop()

def start_client():
    # Conectar al servidor
    client_socket = connect_to_server()
    
    # Pedir el nombre al usuario
    name = input("Introduce tu nombre para unirte al chat: ")
    
    # Enviar nombre al servidor
    client_socket.send(name.encode('utf-8'))
    
    # Crear la interfaz gráfica
    create_gui(client_socket)

if __name__ == "__main__":
    start_client()
