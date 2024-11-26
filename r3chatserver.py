import socket
import threading

HOST = '0.0.0.0'
PORT = 12345
clients = []

def broadcast(message, _client_socket=None):
    for client in clients:
        if client != _client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida con {client_address}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

start_server()

# Coded by R3-K1