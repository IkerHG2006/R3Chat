import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, colorchooser


# Configuración de colores predeterminados
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

# Variables globales para almacenar el tema actual
current_theme = Theme.DARK


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
    window.title(current_theme["title"])

    # Configurar colores de fondo y fuente
    window.configure(bg=current_theme["bg"])

    # Crear cuadro de texto para mostrar los mensajes
    chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=50, height=20, 
                                         bg=current_theme["bg"], fg=current_theme["fg"], font=("Arial", 12))
    chat_box.grid(row=0, column=0, padx=10, pady=10)

    # Crear campo de entrada para escribir mensajes
    entry_field = tk.Entry(window, width=40, font=("Arial", 12), 
                           bg=current_theme["entry_bg"], fg=current_theme["entry_fg"])
    entry_field.grid(row=1, column=0, padx=10, pady=10)

    # Crear botón para enviar el mensaje
    send_button = tk.Button(window, text="Enviar", command=lambda: send_message(client_socket, entry_field),
                            bg=current_theme["btn_bg"], fg=current_theme["btn_fg"], font=("Arial", 12))
    send_button.grid(row=2, column=0, pady=10)

    # Configurar el evento de Enter para enviar el mensaje
    entry_field.bind("<Return>", lambda event: on_enter(client_socket, entry_field))

    # Botón para cambiar entre tema claro y oscuro
    def toggle_theme():
        global current_theme
        if current_theme == Theme.DARK:
            current_theme = Theme.LIGHT
        else:
            current_theme = Theme.DARK
        update_theme(window, client_socket, chat_box, entry_field, send_button)

    theme_button = tk.Button(window, text="Cambiar Tema", command=toggle_theme,
                             bg=current_theme["btn_bg"], fg=current_theme["btn_fg"], font=("Arial", 12))
    theme_button.grid(row=3, column=0, pady=10)

    # Botón para personalizar los colores
    def customize_colors():
        color_dialog = tk.Toplevel(window)
        color_dialog.title("Personalizar Colores")

        def set_custom_colors():
            global current_theme
            bg = colorchooser.askcolor(title="Elige el color de fondo")[1]
            fg = colorchooser.askcolor(title="Elige el color de texto")[1]
            btn_bg = colorchooser.askcolor(title="Elige el color del botón")[1]

            # Si el fondo es oscuro, ponemos el texto blanco, y si es claro, lo ponemos negro
            if bg and fg and btn_bg:
                if is_dark_color(bg):
                    new_fg = "white"
                else:
                    new_fg = "black"
                
                current_theme = {
                    "bg": bg,
                    "fg": new_fg,  # Ajustar el color del texto para que siempre sea visible
                    "btn_bg": btn_bg,
                    "btn_fg": "white",  # Mantener texto de botón blanco
                    "entry_bg": bg,     # El fondo de la entrada será el mismo que el de la ventana
                    "entry_fg": new_fg, # El texto de la entrada será igual que el de la ventana
                    "title": "R3 Chat"
                }
                update_theme(window, client_socket, chat_box, entry_field, send_button)
            color_dialog.destroy()

        apply_button = tk.Button(color_dialog, text="Aplicar Colores", command=set_custom_colors,
                                 bg=current_theme["btn_bg"], fg=current_theme["btn_fg"], font=("Arial", 12))
        apply_button.pack(padx=20, pady=10)

    customize_button = tk.Button(window, text="Personalizar Colores", command=customize_colors,
                                 bg=current_theme["btn_bg"], fg=current_theme["btn_fg"], font=("Arial", 12))
    customize_button.grid(row=4, column=0, pady=10)

    # Iniciar hilo para recibir mensajes
    threading.Thread(target=receive_messages, args=(client_socket, chat_box), daemon=True).start()

    # Ejecutar la interfaz gráfica
    window.mainloop()

# Función para verificar si un color es oscuro
def is_dark_color(color):
    r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]  # Convertir el color hexadecimal a RGB
    brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b  # Fórmula de brillo
    return brightness < 128  # Si el brillo es bajo, el color es oscuro

# Función para actualizar la interfaz gráfica con el nuevo tema
def update_theme(window, client_socket, chat_box, entry_field, send_button):
    window.configure(bg=current_theme["bg"])
    chat_box.configure(bg=current_theme["bg"], fg=current_theme["fg"])
    entry_field.configure(bg=current_theme["entry_bg"], fg=current_theme["entry_fg"])
    send_button.configure(bg=current_theme["btn_bg"], fg=current_theme["btn_fg"])
    window.title(current_theme["title"])

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
