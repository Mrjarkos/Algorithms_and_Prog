import json
import socket
import threading
from functools import partial
from constants import HOST, PORT, ENCODING
from View import AskName, MainWindow

def send_message(conn: socket, data: str):
    try:
        conn.send(data.encode(ENCODING))
    except OSError as e:
        ## Socket was closed
        print("Socket was closed")

def parse_data(data):
    json_str= data.replace("'", "\"")
    line = json.loads(json_str)
    id = int(line["id"])
    time = line["time"]
    name = line["nick"]
    data = line["data"]
    return (time, name, id, data)

def listen_server(conn : socket, show_fct):
    print("Thread-1: Client listening")
    while conn:
        try:
            msg = conn.recv(2048).decode(ENCODING)
            # Decode data
            time, name, id, data = parse_data(msg)
            show_fct(time, name, id, data)
        except OSError as e:
            ## Socket was closed
            print("Thread-1: Socket closes")
            break

if __name__ == '__main__':
    ## Login Window
    name_root = AskName()
    name = name_root.name.get()
    if name == "":
        exit()
        
    # Client Socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) 
        s.send(f"{name}".encode(ENCODING))
        msg = s.recv(2048).decode(ENCODING)
        time, msg_sender, id, data = parse_data(msg)
        ## Main Thread to send
        main = MainWindow(name, id, command=partial(send_message, s))
        
        # Welcome message
        main.send_to_server_chat(time, msg_sender, -1, data)
        
        ## Create a Thread to listen
        thread = threading.Thread(target = listen_server,
                                  args=(s,  main.send_to_server_chat))
        thread.start()
        main.mainloop()
        print("Main-Thread: GUI Client closed")
        
        print("Main-Thread: Closing connection")
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        ## Tell server we are leaving
        print("Main-Thread: Waiting for Thread to finish")
        thread.join(timeout=10)

    print("Main-Thread: Client disconnected")