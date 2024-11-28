import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, colorchooser, filedialog, simpledialog
from tkinter import messagebox
from time import sleep, time
import os
import random

# Tema de colores
class Theme:
    LIGHT = {
        "bg": "#f5f5f5",         # Fondo claro
        "fg": "#333333",         # Texto oscuro
        "btn_bg": "#4CAF50",     # Botón verde
        "btn_fg": "white",       # Texto blanco en botones
        "entry_bg": "#ffffff",   # Fondo de entrada blanco
        "entry_fg": "#333333",   # Texto oscuro en entradas
        "title": "Chat Moderno"
    }
    
    DARK = {
        "bg": "#2c3e50",         # Fondo oscuro
        "fg": "#ecf0f1",         # Texto claro
        "btn_bg": "#3498db",     # Botón azul
        "btn_fg": "white",       # Texto blanco en botones
        "entry_bg": "#34495e",   # Fondo de entrada oscuro
        "entry_fg": "#ecf0f1",   # Texto claro en entradas
        "title": "Chat Oscuro Moderno"
    }

class ChatClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.name = ""
        self.current_theme = Theme.LIGHT
        self.chat_history = []
        self.is_dnd = False  # Variable para Modo No Molestar

        self.window = tk.Tk()
        self.chat_box = None
        self.entry_field = None
        self.send_button = None
        self.status_label = None
        self.notification_flag = False
        self.volume = 1  # Volumen de notificaciones

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")
            self.window.quit()
    
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message and not self.is_dnd:
                    self.chat_history.append(message)
                    self.chat_box.insert(tk.END, f"{message}\n")
                    self.chat_box.yview(tk.END)
                    if not self.notification_flag:
                        self.status_label.config(text="¡Nuevo mensaje!", fg="red")
                        self.notification_flag = True
                        if self.volume > 0:
                            # Simula un sonido con una pequeña vibración del UI
                            self.window.bell()
            except:
                break

    def send_message(self):
        message = self.entry_field.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.chat_history.append(f"{self.name}: {message}")
            self.entry_field.delete(0, tk.END)
            self.status_label.config(text="Mensaje enviado", fg="green")
            self.notification_flag = False

    def on_enter(self, event=None):
        self.send_message()

    def toggle_theme(self):
        self.current_theme = Theme.DARK if self.current_theme == Theme.LIGHT else Theme.LIGHT
        self.update_theme()

    def customize_colors(self):
        color_dialog = tk.Toplevel(self.window)
        color_dialog.title("Personalizar Colores")

        def set_custom_colors():
            bg = colorchooser.askcolor(title="Elige el color de fondo")[1]
            fg = colorchooser.askcolor(title="Elige el color de texto")[1]
            btn_bg = colorchooser.askcolor(title="Elige el color del botón")[1]

            if bg and fg and btn_bg:
                new_fg = "white" if self.is_dark_color(bg) else "black"
                self.current_theme = {
                    "bg": bg,
                    "fg": new_fg,
                    "btn_bg": btn_bg,
                    "btn_fg": "white",
                    "entry_bg": bg,
                    "entry_fg": new_fg,
                    "title": "R3 Chat"
                }
                self.update_theme()
            color_dialog.destroy()

        apply_button = tk.Button(color_dialog, text="Aplicar Colores", command=set_custom_colors,
                                 bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"],
                                 font=("Helvetica", 12), relief="flat", activebackground=self.current_theme["btn_bg"],
                                 activeforeground="white")
        apply_button.pack(padx=20, pady=10)

    def is_dark_color(self, color):
        r, g, b = [int(color[i:i+2], 16) for i in (1, 3, 5)]  
        brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return brightness < 128

    def update_theme(self):
        self.window.configure(bg=self.current_theme["bg"])
        self.chat_box.configure(bg=self.current_theme["bg"], fg=self.current_theme["fg"])
        self.entry_field.configure(bg=self.current_theme["entry_bg"], fg=self.current_theme["entry_fg"])
        self.send_button.configure(bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"])
        self.status_label.configure(bg=self.current_theme["bg"], fg=self.current_theme["fg"])
        self.window.title(self.current_theme["title"])

    def add_emoji(self):
        emojis = ["😊", "😂", "😎", "😍", "🤔", "🙌", "💥"]
        emoji = random.choice(emojis)
        self.entry_field.insert(tk.END, emoji)

    def toggle_dnd(self):
        self.is_dnd = not self.is_dnd
        if self.is_dnd:
            self.status_label.config(text="Modo No Molestar Activado", fg="yellow")
        else:
            self.status_label.config(text="Modo No Molestar Desactivado", fg="green")

    def attach_file(self):
        file_path = filedialog.askopenfilename(title="Selecciona un archivo")
        if file_path:
            self.chat_box.insert(tk.END, f"[Archivo adjunto: {os.path.basename(file_path)}]\n")
            self.chat_box.yview(tk.END)

    def schedule_message(self):
        time_str = simpledialog.askstring("Programar Mensaje", "Escribe el tiempo en segundos para el mensaje:")
        if time_str:
            try:
                delay = int(time_str)
                message = simpledialog.askstring("Escribe tu mensaje", "Tu mensaje:")
                if message:
                    sleep(delay)
                    self.client_socket.send(message.encode('utf-8'))
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa un número válido.")

    def create_gui(self):
        self.window.title(self.current_theme["title"])
        self.window.configure(bg=self.current_theme["bg"])

        self.chat_box = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=60, height=20, 
                                                  bg=self.current_theme["bg"], fg=self.current_theme["fg"], 
                                                  font=("Helvetica", 12), bd=0)
        self.chat_box.grid(row=0, column=0, padx=20, pady=10)

        self.entry_field = tk.Entry(self.window, width=40, font=("Helvetica", 12), 
                                    bg=self.current_theme["entry_bg"], fg=self.current_theme["entry_fg"], 
                                    bd=0, relief="flat")
        self.entry_field.grid(row=1, column=0, padx=20, pady=10)
        self.entry_field.bind("<Return>", self.on_enter)

        self.send_button = tk.Button(self.window, text="Enviar", command=self.send_message,
                                     bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"], 
                                     font=("Helvetica", 12), relief="flat", activebackground=self.current_theme["btn_bg"],
                                     activeforeground="white")
        self.send_button.grid(row=2, column=0, pady=10)

        self.status_label = tk.Label(self.window, text="", bg=self.current_theme["bg"], fg=self.current_theme["fg"],
                                     font=("Helvetica", 10))
        self.status_label.grid(row=3, column=0, pady=10)

        theme_button = tk.Button(self.window, text="Cambiar Tema", command=self.toggle_theme,
                                 bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"], 
                                 font=("Helvetica", 12), relief="flat", activebackground=self.current_theme["btn_bg"],
                                 activeforeground="white")
        theme_button.grid(row=4, column=0, pady=10)

        emoji_button = tk.Button(self.window, text="Añadir Emoji", command=self.add_emoji,
                                 bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"],
                                 font=("Helvetica", 12), relief="flat", activebackground=self.current_theme["btn_bg"],
                                 activeforeground="white")
        emoji_button.grid(row=5, column=0, pady=10)

        dnd_button = tk.Button(self.window, text="Modo No Molestar", command=self.toggle_dnd,
                               bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"],
                               font=("Helvetica", 12), relief="flat", activebackground=self.current_theme["btn_bg"],
                               activeforeground="white")
        dnd_button.grid(row=6, column=0, pady=10)

        file_button = tk.Button(self.window, text="Adjuntar Archivo", command=self.attach_file,
                                bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"],
                                font=("Helvetica", 12), relief="flat", activebackground=self.current_theme["btn_bg"],
                                activeforeground="white")
        file_button.grid(row=7, column=0, pady=10)

        schedule_button = tk.Button(self.window, text="Programar Mensaje", command=self.schedule_message,
                                    bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"],
                                    font=("Helvetica", 12), relief="flat", activebackground=self.current_theme["btn_bg"],
                                    activeforeground="white")
        schedule_button.grid(row=8, column=0, pady=10)

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def request_name(self):
        self.name = simpledialog.askstring("Nombre", "Introduce tu nombre:")
        if self.name:
            self.client_socket.send(self.name.encode('utf-8'))

    def start_client(self):
        self.connect_to_server()
        self.request_name()
        self.create_gui()
        self.window.mainloop()


if __name__ == "__main__":
    client = ChatClient('192.168.1.82', 12345)  # Cambiar la IP a la correcta
    client.start_client()
