import socket
import threading
import sys
import os

# Función para recibir mensajes del servidor
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\033[1;37;40m{message}\033[0m")  # Mostrar mensaje con estilo oscuro
            else:
                break
        except:
            break

# Función para limpiar la terminal (más limpia visualmente)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Configuración del cliente
def start_client():
    clear()
    name = input("Introduce tu nombre para unirte al chat: ")  # Pide el nombre del usuario
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.100', 12345))  # Usa la IP real del servidor
    
    client.send(name.encode('utf-8'))  # Enviar el nombre al servidor

    # Iniciar hilo para recibir mensajes
    threading.Thread(target=receive_messages, args=(client,)).start()

    print(f"\033[1;37;40m¡Bienvenido al chat, {name}!\033[0m")
    print("\033[1;37;40mEscribe tu mensaje y presiona Enter para enviarlo.\033[0m")

    while True:
        message = input()  # Leer mensaje
        if message:
            client.send(message.encode('utf-8'))  # Enviar mensaje al servidor

if __name__ == "__main__":
    start_client()
