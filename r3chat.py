import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '192.168.1.82'
PORT = 12345

# Función para pedir el nombre de usuario al iniciar
def ask_username():
    def set_username():
        global username
        username = name_entry.get()
        if username.strip():
            username_window.destroy()
            connect_to_server()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre válido.")

    username_window = tk.Tk()
    username_window.title("Ingrese su nombre")

    tk.Label(username_window, text="Nombre de usuario:", font=("Helvetica", 12)).pack(pady=10)
    name_entry = tk.Entry(username_window, font=("Helvetica", 12))
    name_entry.pack(pady=5)
    
    tk.Button(username_window, text="Conectar", command=set_username, bg="#1abc9c", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(pady=20)
    
    username_window.mainloop()

# Inicialización de la conexión al servidor
def connect_to_server():
    global connected
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(username.encode())  # Enviar el nombre al servidor
        connected = True
        status_label.config(text="Conectado", bg="#27ae60", fg="#ffffff")
        toggle_input()
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
        connected = False
        status_label_text = "Desconectado"

# Mostrar el mensaje en el chat
def display_message(message, is_sent=True):
    chat_area.config(state=tk.NORMAL)
    
    if is_sent:
        chat_area.insert(tk.END, f"{username}: {message}\n", "sent")
    else:
        chat_area.insert(tk.END, f"{message}\n", "received")
        
    chat_area.yview(tk.END)
    chat_area.config(state=tk.DISABLED)

# Función para recibir mensajes del servidor
def receive_messages():
    global connected
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                display_message(message, is_sent=False)
            else:
                connected = False
                status_label.config(text="Desconectado", bg="#e74c3c", fg="#ffffff")
                toggle_input()
                break
        except:
            messagebox.showerror("Error", "Conexión perdida con el servidor.")
            connected = False
            status_label.config(text="Desconectado", bg="#e74c3c", fg="#ffffff")
            toggle_input()
            break

# Función para enviar un mensaje al servidor
def send_message(event=None):
    if connected:
        message = message_input.get()
        if message.strip():
            display_message(message, is_sent=True)
            client_socket.send(message.encode())
            message_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "No puedes enviar un mensaje vacío.")
    else:
        messagebox.showwarning("Advertencia", "No estás conectado al servidor.")

# Función para reconectar al servidor
def reconnect():
    global connected
    try:
        client_socket.connect((HOST, PORT))
        connected = True
        status_label.config(text="Conectado", bg="#27ae60", fg="#ffffff")
        toggle_input()
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reconectar: {e}")
        threading.Timer(5.0, reconnect).start()

# Función para cerrar la conexión
def on_close():
    try:
        client_socket.close()
    except:
        pass
    root.quit()

# Función para desconectar
def disconnect():
    global connected
    try:
        client_socket.close()
        connected = False
        status_label.config(text="Desconectado", bg="#e74c3c", fg="#ffffff")
        toggle_input()
        disconnect_button.config(text="Conectar", command=reconnect)
        messagebox.showinfo("Desconectado", "Te has desconectado correctamente.")
    except:
        messagebox.showerror("Error", "Hubo un problema al desconectarte.")
        
# Habilitar/deshabilitar la entrada de mensajes
def toggle_input():
    if connected:
        message_input.config(state=tk.NORMAL)
        send_button.config(state=tk.NORMAL)
    else:
        message_input.config(state=tk.DISABLED)
        send_button.config(state=tk.DISABLED)

# Función principal para ejecutar el cliente
def main():
    global client_socket, connected, username, status_label, status_label_text

    ask_username()  # Pedir el nombre del usuario al inicio

    root = tk.Tk()
    root.title("R3 Chat")

    root.geometry("600x500")
    root.configure(bg="#2c3e50")

    title_label = tk.Label(root, text="R3 Chat", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
    title_label.pack(pady=20)

    frame = tk.Frame(root, bg="#34495e", bd=2, relief="sunken")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=15, state=tk.DISABLED, bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 11), bd=0, insertbackground='white')
    chat_area.pack(pady=10, padx=10)

    message_input = tk.Entry(frame, width=45, bg="#34495e", fg="#ecf0f1", font=("Helvetica", 12), bd=0, relief="flat", insertbackground='white')
    message_input.pack(side=tk.LEFT, padx=(10, 10), pady=(0, 10))

    send_button = tk.Button(frame, text="Enviar", command=send_message, bg="#1abc9c", fg="#ffffff", font=("Helvetica", 12, "bold"), bd=0, relief="flat")
    send_button.pack(side=tk.LEFT, padx=10, pady=(0, 10))

    status_label = tk.Label(root, text="Desconectado", bg="#e74c3c", fg="#ffffff", font=("Helvetica", 12), relief="flat")
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    disconnect_button = tk.Button(root, text="Desconectar", command=disconnect, bg="#e74c3c", fg="#ffffff", font=("Helvetica", 12, "bold"), bd=0, relief="flat")
    disconnect_button.pack(pady=10)

    message_input.bind('<Return>', send_message)

    root.protocol("WM_DELETE_WINDOW", on_close)

    if connected:
        threading.Thread(target=receive_messages, daemon=True).start()

    toggle_input()

    root.mainloop()

if __name__ == "__main__":
    main()
