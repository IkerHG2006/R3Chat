import socket
import threading

HOST = '0.0.0.0'
PORT = 12345
clients = []

def broadcast(message, client_name, _client_socket=None):
    for client, name in clients:
        if client != _client_socket:
            try:
                client.send(f"{name}: {message}".encode())
            except:
                clients.remove(client)

def handle_client(client_socket, client_name):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(message, client_name, client_socket)
            else:
                break
        except:
            clients.remove((client_socket, client_name))
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_name = client_socket.recv(1024).decode('utf-8')  # Recibir el nombre de usuario
        print(f"Conexión establecida con {client_address} - Nombre del cliente: {client_name}")
        
        clients.append((client_socket, client_name))
        threading.Thread(target=handle_client, args=(client_socket, client_name)).start()

start_server()
