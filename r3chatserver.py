import socket
import threading

clients = []  # Lista de conexiones activas
usernames = set()  # Nombres de usuario conectados

def handle_client(client_socket, addr):
    global clients, usernames
    try:
        # Recibir el nombre de usuario
        username = client_socket.recv(1024).decode('utf-8')

        # Verificar si el nombre ya está en uso
        if username in usernames:
            client_socket.send("Nombre en uso".encode('utf-8'))
            client_socket.close()
            return
        else:
            usernames.add(username)
            client_socket.send("Nombre aceptado".encode('utf-8'))

        # Anunciar al chat
        broadcast(f"{username} se ha unido al chat.", client_socket)

        # Manejar mensajes
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(f"{username}: {message}", client_socket)
            else:
                break
    except:
        pass
    finally:
        # Eliminar al cliente al desconectar
        if username in usernames:
            usernames.remove(username)
        clients.remove(client_socket)
        client_socket.close()
        broadcast(f"{username} ha salido del chat.", None)

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("Servidor escuchando en el puerto 12345...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    main()
