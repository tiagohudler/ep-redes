import socket, pickle
import message

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = pickle.loads(s.recv(1024))
    if data.code == 0:
        print("Waiting for opponent")
        data = s.recv(1024)
    print("Game start:\nPossible actions: DEFEND, SHOOT, RELOAD\nEach player starts with 3 lives and 1 bullet\nGood luck!")
    
    while True:
        data = pickle.loads(s.recv(1024))
        if data.code == 2:
            print(data.message)
            print("Bullets: ", data.bullets)
            action = input("Enter your action: ")
            s.sendall(pickle.dumps(message.message(2, action, "")))
        elif data.code == 1:
            print("Acabou a rodada")
            print(data.message)
            break
        
        elif data.code == 3:
            print(data.message)
            break
        else:
            print("Invalid message")
            break
