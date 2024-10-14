import socket, pickle
import message
import threading
import tkinter as tk

#HOST = "192.168.15.9"
#HOST = "192.168.15.85"
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def send_chat(sock):
    message = input_field.get()
    chat_box.config(state=tk.NORMAL) 
    chat_box.insert(tk.END, "You: " + message + "\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)
    sock.send(message.encode())
    input_field.delete(0, tk.END)

# Função para configurar a janela do chat
def start_chat_interface():
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket.connect((HOST, PORT))

    def receive_chat():
        while True:
            try:
                message = chat_socket.recv(1024).decode()
                if message:
                    chat_box.config(state=tk.NORMAL) 
                    chat_box.insert(tk.END, message + "\n")
                    chat_box.config(state=tk.DISABLED)
                    chat_box.see(tk.END)
            except:
                break
    
    global chat_box, input_field

    window = tk.Tk()
    window.title("Game Chat")

    chat_box = tk.Text(window, height=15, width=50)
    chat_box.pack()
    chat_box.config(state=tk.DISABLED)

    input_field = tk.Entry(window, width=50)
    input_field.pack()

    send_button = tk.Button(window, text="Send", command=lambda: send_chat(chat_socket))
    send_button.pack()

    threading.Thread(target=receive_chat, args=(), daemon=True).start()

    window.mainloop()

def receive_full_message(sock):
    buffer = b""
    while True:
        data = sock.recv(1024)
        buffer += data
        try:
            return pickle.loads(buffer) 
        except (pickle.UnpicklingError, EOFError):
            
            continue
        
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((HOST, PORT))

threading.Thread(target=start_chat_interface, args=(), daemon=True).start()

data = pickle.loads(server_socket.recv(1024))

if data.code == 0:
    print("Waiting for opponent")
    data = server_socket.recv(1024)

print(
    "#############################################################################################################\n"
    "GAME RULES\n"
    "#############################################################################################################\n"
    "Possible actions: DEFEND, SHOOT, RELOAD\nEach player starts with 3 lives and 1 bullet\n"
    "If a player shoots and the other player doesn't defend, the player that took the shot loses a life\n"
    "Whenever a player is shot, both players go back to only one bullet\n"
    "The first player to take 3 lives from the other wins the round\n"
    "If both players shoot, they both lose a life\n"
    "If both the players lose all their lives, the round is a draw, and no one wins a point\n"
    "The first one to 2 rounds wins\n"
    "Good luck!\n"
    "#############################################################################################################\n"
    "Game start:\n"
)

server_socket.sendall(b"Ready to play")

while True:

    data = pickle.loads(server_socket.recv(1024))
    
    if data.code == 2:
        print(
            "###############################################\n"+
            data.message
        )
        print("Bullets: ", data.bullets)
        while True:
            action = input("Enter your action: ")
            if (action != "DEFEND" and action != "SHOOT" and action != "RELOAD"):
                print("Invalid action")
            elif (action == "SHOOT" and data.bullets == 0):
                print("You can only shoot if you have bullets.")
            else:
                break
        print("###############################################\n")
        server_socket.sendall(pickle.dumps(message.message(2, action, "")))
    elif data.code == 1:
        print(data.message)
        print("\n###############################################\n")
        action = input("Enter your action: ")
        server_socket.sendall(pickle.dumps(message.message(2, action, "")))
    
    elif data.code == 3:
        print(data.message)
        response = input()
        if response == 'y':
            server_socket.sendall(pickle.dumps(message.message(1, "", "")))
        else:
            server_socket.sendall(pickle.dumps(message.message(3, "", "")))
        data = pickle.loads(server_socket.recv(1024))

        if data.code == 3:
            print(data.message)
            break
        else:
            print("\n###############################################\n"+data.message)
            action = input("Enter your action: ")
            server_socket.sendall(pickle.dumps(message.message(2, action, "")))

    else:
        print("Invalid message")
        break
