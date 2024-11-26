import socket
import threading

# Lista para almacenar los clientes conectados
clients = []

# Función para manejar la comunicación con cada cliente
def handle_client(client_socket, client_address):
    try:
        # Pedimos el nombre del cliente
        client_socket.send("Introduce tu nombre:".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8')
        
        # Notificar a todos los clientes sobre la conexión
        welcome_message = f"{name} se ha unido al chat."
        broadcast(welcome_message, client_socket)

        print(f"Nuevo usuario conectado: {name} desde {client_address}")
        
        # Añadir el cliente a la lista de clientes
        clients.append((client_socket, name))

        # Continuar recibiendo y enviando mensajes
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Enviar mensaje a todos los clientes
                broadcast(f"{name}: {message}", client_socket)
            else:
                break
    except Exception as e:
        print(f"Error con el cliente {client_address}: {e}")
    finally:
        # Eliminar cliente de la lista y cerrar la conexión
        clients.remove((client_socket, name))
        client_socket.close()
        broadcast(f"{name} se ha desconectado.", client_socket)

# Función para enviar un mensaje a todos los clientes conectados
def broadcast(message, client_socket):
    for client, _ in clients:
        if client != client_socket:  # No enviarlo al cliente que lo envió
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Función para iniciar el servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.1.82', 12345))  # Cambia esta IP a la de tu servidor
    server.listen(5)

    print("Servidor escuchando en 192.168.1.82:12345...")

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
