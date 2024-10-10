import socket, pickle
import message
import threading
import tkinter as tk

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def receive_chat(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                chat_box.insert(tk.END, message + "\n")
        except:
            break

def send_chat(sock):
    message = input_field.get()
    chat_box.insert(tk.END, "Você: " + message + "\n")
    sock.send(message.encode())
    input_field.delete(0, tk.END)

# Função para configurar a janela do chat
def start_chat_interface(sock):
    global chat_box, input_field

    window = tk.Tk()
    window.title("Chat do Jogo")

    chat_box = tk.Text(window, height=15, width=50)
    chat_box.pack()

    input_field = tk.Entry(window, width=50)
    input_field.pack()

    send_button = tk.Button(window, text="Enviar", command=lambda: send_chat(sock))
    send_button.pack()

    threading.Thread(target=receive_chat, args=(sock,)).start()
    threading.Thread(target=send_chat, args=(sock,)).start()

    window.mainloop()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat.connect((HOST, PORT))
    
    threading.Thread(target=start_chat_interface, args=(chat,)).start()

    data = pickle.loads(s.recv(1024))
    if data.code == 0:
        print("Waiting for opponent")
        data = s.recv(1024)
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

    bullets = 1
    
    while True:
        data = pickle.loads(s.recv(1024))
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
            s.sendall(pickle.dumps(message.message(2, action, "")))
        elif data.code == 1:
            print(data.message)
            print("\n###############################################\n")
            action = input("Enter your action: ")
            s.sendall(pickle.dumps(message.message(2, action, "")))
        
        elif data.code == 3:
            print(data.message)
            response = input()
            if response == 'y':
                s.sendall(pickle.dumps(message.message(1, "", "")))
            else:
                s.sendall(pickle.dumps(message.message(3, "", "")))
            data = pickle.loads(s.recv(1024))

            if data.code == 3:
                print(data.message)
                break
            else:
                print("\n###############################################\n"+data.message)
                action = input("Enter your action: ")
                s.sendall(pickle.dumps(message.message(2, action, "")))

        else:
            print("Invalid message")
            break
