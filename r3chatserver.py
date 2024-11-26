import socket
import threading

# Lista para almacenar las conexiones de los clientes
clients = []

# Función para manejar la recepción de mensajes
def handle_client(client_socket, client_address):
    # Obtener el nombre del cliente
    name = client_socket.recv(1024).decode('utf-8')  
    print(f"{name} se ha unido al chat.")
    
    # Añadir el cliente a la lista
    clients.append((client_socket, name))
    
    # Enviar un mensaje de bienvenida a ese cliente
    client_socket.send(f"¡Bienvenido al chat, {name}!".encode('utf-8'))
    
    while True:
        try:
            # Recibe el mensaje del cliente
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{name}: {message}")
                # Enviar el mensaje a todos los demás clientes
                broadcast(message, name)
            else:
                break
        except:
            break
    
    # Eliminar al cliente cuando se desconecte
    clients.remove((client_socket, name))
    client_socket.close()

# Función para enviar el mensaje a todos los clientes
def broadcast(message, name):
    for client, _ in clients:
        try:
            client.send(f"{name}: {message}".encode('utf-8'))
        except:
            continue

# Configuración del servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))  # Dirección y puerto del servidor
    server.listen(5)
    print("Servidor escuchando en el puerto 12345...")

    while True:
        client_socket, client_address = server.accept()
        print(f"Conexión de {client_address}")
        
        # Hilo para manejar a cada cliente
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
