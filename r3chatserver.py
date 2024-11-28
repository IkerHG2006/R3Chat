import socket
import threading

clients = {}
lock = threading.Lock()

def handle_client(client_socket, client_address):
    name = client_socket.recv(1024).decode('utf-8')
    with lock:
        clients[client_socket] = name
    print(f"{name} se ha unido desde {client_address}.")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith("/users"):
                user_list = ",".join([n for s, n in clients.items() if s != client_socket])
                client_socket.send(user_list.encode('utf-8'))
            elif ":" in message:
                target, msg = message.split(":", 1)
                with lock:
                    if target in clients.values():
                        for s, n in clients.items():
                            if n == target:
                                s.send(f"(Privado) {clients[client_socket]}: {msg}".encode('utf-8'))
                                break
                    else:
                        broadcast(message, client_socket)
            else:
                broadcast(message, client_socket)
        except:
            with lock:
                del clients[client_socket]
            client_socket.close()
            break

def broadcast(message, sender_socket):
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(f"{clients[sender_socket]}: {message}".encode('utf-8'))
                except:
                    client.close()
                    del clients[client]

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Servidor escuchando en el puerto 12345...")

    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()

if __name__ == "__main__":
    start_server()
