import socket
import threading

# Configuración del servidor
HOST = '192.168.1.82'  # Cambia a tu IP
PORT = 12345
clients = []

# Enviar mensaje a todos los clientes conectados
def broadcast_message(message, client):
    for c in clients:
        if c != client:
            try:
                c.send(message.encode())
            except:
                clients.remove(c)

# Manejar mensajes de un cliente
def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                broadcast_message(message, client)
        except:
            clients.remove(client)
            break

# Conectar y escuchar clientes
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor iniciado en {HOST}:{PORT}")
    
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"Nuevo cliente conectado: {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == '__main__':
    start_server()
