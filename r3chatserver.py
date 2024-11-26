import socket
import threading

# Lista para almacenar los clientes conectados
clients = []

# Función para manejar la comunicación con cada cliente
def handle_client(client_socket):
    while True:
        try:
            # Recibimos el mensaje del cliente
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Enviamos el mensaje a todos los clientes conectados
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

# Función para enviar un mensaje a todos los clientes
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Configuración del servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.1.82', 12345))  # IP local del servidor
    server.listen(5)
    print("Servidor escuchando en el puerto 12345...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Conexión de {addr}")
        
        # Pedimos el nombre del cliente
        client_socket.send("Introduce tu nombre:".encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8')
        
        clients.append(client_socket)
        client_socket.send(f"Bienvenido, {name}!".encode('utf-8'))
        
        # Iniciamos un hilo para manejar al cliente
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
