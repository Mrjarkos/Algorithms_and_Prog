import socket
import threading

def process(conn):
    while True:
        data = conn.recv(2048).decode()
        if not data:
            # if data is not received, break
            break
        print(f"Data received: {data.decode()}")
        if data == "1":
            conn.send("Hola Amigo")
        elif data == "2":
            conn.send("Acceso Denegado!")
        else:
            conn.send(data.encode())
    conn.close()

def server_program():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()  
    server_socket.bind((host, port)) 
    
    server_socket.listen(5)
    
    while True:
        conn, address = server_socket.accept() 
        print("Connection from: " + str(address))
        thread = threading.Thread(target = process, args=(conn))
        thread.start()

if __name__ == '__main__':
    server_program()
