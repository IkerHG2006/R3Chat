import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, colorchooser

# Configuración de colores predeterminados
class Theme:
    DARK = {
        "bg": "black",
        "fg": "white",
        "btn_bg": "#4CAF50",
        "btn_fg": "white",
        "entry_bg": "#2a2a2a",
        "entry_fg": "white",
        "title": "R3 Chat - Tema Oscuro"
    }
    LIGHT = {
        "bg": "white",
        "fg": "black",
        "btn_bg": "#008CBA",
        "btn_fg": "white",
        "entry_bg": "#f1f1f1",
        "entry_fg": "black",
        "title": "R3 Chat - Tema Claro"
    }

# Variables globales
current_theme = Theme.DARK
username = None  # Para almacenar el nombre del usuario


# Conexión al servidor
def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.82', 12345))  # Cambiar IP al servidor real
    return client_socket


# Obtener lista de usuarios activos del servidor
def fetch_users(client_socket):
    try:
        client_socket.send("/users".encode('utf-8'))  # Solicita usuarios al servidor
        users = client_socket.recv(1024).decode('utf-8').split(",")
        return [user for user in users if user and user != username]  # Excluir el propio usuario
    except:
        return []


# Ventana principal con selección de chats
def main_window(client_socket):
    window = tk.Tk()
    window.title(current_theme["title"])
    window.geometry("400x300")
    window.configure(bg=current_theme["bg"])

    # Etiqueta de bienvenida
    welcome_label = tk.Label(
        window,
        text=f"Bienvenido a R3Chat, {username}",
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        font=("Arial", 16),
    )
    welcome_label.pack(pady=20)

    # Botón para entrar al chat general
    def join_general_chat():
        window.destroy()
        create_chat_window(client_socket, "General", width=600, height=500)

    general_button = tk.Button(
        window,
        text="Chat General",
        command=join_general_chat,
        bg=current_theme["btn_bg"],
        fg=current_theme["btn_fg"],
        font=("Arial", 12),
    )
    general_button.pack(pady=10)

    # Botón para abrir lista de usuarios conectados y elegir chat privado
    def open_private_chat():
        users = fetch_users(client_socket)

        if not users:  # Si no hay usuarios activos
            messagebox.showinfo("Usuarios", "No hay usuarios conectados en este momento.")
            return

        # Crear ventana para seleccionar usuario
        chat_selection_window = tk.Toplevel(window)
        chat_selection_window.title("Usuarios Conectados")
        chat_selection_window.configure(bg=current_theme["bg"])

        # Lista de usuarios
        user_listbox = tk.Listbox(
            chat_selection_window,
            bg=current_theme["entry_bg"],
            fg=current_theme["entry_fg"],
        )
        for user in users:
            user_listbox.insert(tk.END, user)
        user_listbox.pack(padx=10, pady=10)

        # Botón para iniciar el chat privado
        def start_private_chat():
            selected_user = user_listbox.get(tk.ACTIVE)
            if selected_user:
                chat_selection_window.destroy()
                create_chat_window(client_socket, selected_user, is_private=True, width=700, height=600)

        private_chat_button = tk.Button(
            chat_selection_window,
            text="Abrir Chat Privado",
            command=start_private_chat,
            bg=current_theme["btn_bg"],
            fg=current_theme["btn_fg"],
        )
        private_chat_button.pack(pady=5)

    private_button = tk.Button(
        window,
        text="Chat Privado",
        command=open_private_chat,
        bg=current_theme["btn_bg"],
        fg=current_theme["btn_fg"],
        font=("Arial", 12),
    )
    private_button.pack(pady=10)

    # Botón para cambiar entre tema claro y oscuro
    def toggle_theme():
        global current_theme
        current_theme = Theme.LIGHT if current_theme == Theme.DARK else Theme.DARK
        update_theme(window)

    theme_button = tk.Button(
        window,
        text="Cambiar Tema",
        command=toggle_theme,
        bg=current_theme["btn_bg"],
        fg=current_theme["btn_fg"],
        font=("Arial", 12),
    )
    theme_button.pack(pady=10)

    # Ejecutar ventana principal
    window.mainloop()


# Crear ventana de chat
def create_chat_window(client_socket, chat_name, is_private=False, width=600, height=500):
    window = tk.Tk()
    window.title(f"R3Chat - {chat_name}")
    window.geometry(f"{width}x{height}")
    window.configure(bg=current_theme["bg"])

    # Crear cuadro de texto para mostrar mensajes
    chat_box = scrolledtext.ScrolledText(
        window,
        wrap=tk.WORD,
        width=70,
        height=25,
        bg=current_theme["bg"],
        fg=current_theme["fg"],
        font=("Arial", 12),
    )
    chat_box.grid(row=0, column=0, padx=10, pady=10)

    # Crear campo de entrada para escribir mensajes
    entry_field = tk.Entry(
        window,
        width=50,
        font=("Arial", 12),
        bg=current_theme["entry_bg"],
        fg=current_theme["entry_fg"],
    )
    entry_field.grid(row=1, column=0, padx=10, pady=10)

    # Función para enviar mensaje
    def send_message():
        message = entry_field.get()
        if message:
            chat_type = "/private" if is_private else "/general"
            client_socket.send(f"{chat_type}:{chat_name}:{message}".encode('utf-8'))
            entry_field.delete(0, tk.END)

    send_button = tk.Button(
        window,
        text="Enviar",
        command=send_message,
        bg=current_theme["btn_bg"],
        fg=current_theme["btn_fg"],
        font=("Arial", 12),
    )
    send_button.grid(row=2, column=0, pady=10)

    # Función para recibir mensajes
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                chat_box.insert(tk.END, f"{message}\n")
                chat_box.yview(tk.END)
            except:
                break

    # Iniciar hilo para recibir mensajes
    threading.Thread(target=receive_messages, daemon=True).start()

    # Configurar evento Enter para enviar mensaje
    entry_field.bind("<Return>", lambda _: send_message())

    window.mainloop()


# Actualizar tema en la interfaz
def update_theme(window):
    window.configure(bg=current_theme["bg"])


# Inicio del cliente
def start_client():
    global username
    client_socket = connect_to_server()

    # Solicitar nombre al usuario
    username = input("Introduce tu nombre para unirte al chat: ")
    client_socket.send(username.encode('utf-8'))  # Enviar nombre al servidor

    # Abrir ventana principal
    main_window(client_socket)


if __name__ == "__main__":
    start_client()
