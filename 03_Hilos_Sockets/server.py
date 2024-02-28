import time
import atexit
import socket
import threading
from constants import HOST, PORT, ENCODING

class Client():
    
    def __init__(self, conn: socket.socket, addr, nick:str, id:int):
        self.conn = conn
        self.addr = addr
        self.nick = nick
        self.id = id

clients: list[Client] = []

def notify_all(msg):
    print(msg)
    for cl in clients:
        try:
            cl.conn.send(f"{msg}".encode(ENCODING))
        except OSError as e:
        ## Socket was closed
            print(f"Socket {cl.id} was closed")

def logging(client: Client):
    global clients
    print(f"[{client.id}] Thread {client.id} listening...")
    while True:
        data = client.conn.recv(2048).decode(ENCODING)
        if not data:
            # if data is not received, break
            break
        # Console Logging
        print(f"[{client.id}] {client.nick} says: {data}")
        # Broadcast Info
        info_dict = {
            "id" : client.id,
            "nick": client.nick,
            "time": time.strftime("%H:%M", time.localtime()),
            "data" : data
        }
        notify_all(info_dict)
    
    ## Finish Connection
    client.conn.shutdown(socket.SHUT_RDWR)
    client.conn.close()
    idx = clients.index(client)
    clients.pop(idx)
    info_dict = {
    "id" : -1,
    "nick": "Server",
    "time": time.strftime("%H:%M", time.localtime()),
    "data" : f"{client.nick} se ha desconectado"
    }
    notify_all(info_dict)

def accept_client(s : socket.socket):
    id = 0
    global clients
    ## Wait for client to connect
    while s:
        conn, address = s.accept() 
        print("Connection from: " + str(address))

        # Protocol:
        # Client has to send the Nickname
        nick = conn.recv(2048).decode()
        # Server replies with the Id
        info_dict = {
        "id" : id,
        "nick": "Server",
        "time": time.strftime("%H:%M", time.localtime()),
        "data" : f"Welcome: {nick}[{id}]"
        }
        conn.send(f"{info_dict}".encode(ENCODING))
        # Client starts chatting

        info_dict = {
        "id" : -1,
        "nick": "Server",
        "time": time.strftime("%H:%M", time.localtime()),
        "data" : f"{nick}[{id}] ha entrado al chat"
        }
        notify_all(info_dict)

        cl = Client(conn, address, nick, id)
        clients.append(cl)
        id+=1
        thread = threading.Thread(target = logging, args=(cl,))
        thread.start()

def server_program():
    ## Use context for error handling
    # AF_INET -> IPv4
    # SOCK_STREAM -> Default TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) 
        s.listen()
        print(f"Server starting: {HOST}:{PORT}")
        try:
            thread = threading.Thread(target = accept_client, args=(s,))
            thread.start()
            while True:
                ## Wait for keyboard interrupt
                pass
            
        except KeyboardInterrupt:
            # Code to execute when Ctrl+C is pressed
            ## Close all clients
            print("Program terminated by user.")
        
        except OSError as e:
            print("Socket was closed\n")
            print(e)
        finally:
            cleanup()
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            exit()

def cleanup():
    print("Cleanup function executed.")
    info_dict = {
            "id" : -1,
            "nick": "Server",
            "time": time.strftime("%H:%M", time.localtime()),
            "data" : ""
            }
    notify_all(info_dict)

# If console is closed externally
atexit.register(cleanup)

if __name__ == '__main__':    
    server_program()
    