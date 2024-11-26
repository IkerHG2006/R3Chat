import socket
import threading

clients = []

# Función para manejar la recepción de mensajes
def handle_client(client_socket, client_address):
    name = client_socket.recv(1024).decode('utf-8')  # Obtener nombre
    print(f"{name} se ha unido al chat.")
    
    clients.append((client_socket, name))
    
    # Enviar mensaje de bienvenida
    client_socket.send(f"¡Bienvenido al chat, {name}!".encode('utf-8'))
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{name}: {message}")
                broadcast(message, name)
            else:
                break
        except:
            break
    
    clients.remove((client_socket, name))
    client_socket.close()

# Función para enviar mensajes a todos los clientes
def broadcast(message, name):
    for client, _ in clients:
        try:
            client.send(f"{name}: {message}".encode('utf-8'))
        except:
            continue

# Configuración del servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Servidor escuchando en el puerto 12345...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Conexión de {client_address}")
        
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
