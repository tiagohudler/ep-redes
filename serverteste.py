import socket
import game
import message

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:


    s.bind((HOST, PORT))
    s.listen(2)
    print("Waiting for players to connect")
    client1, addr1 = s.accept()
    client1.sendall(b"Waiting for opponent to connect")
    print("Player 1 connected. Waiting for player 2 to connect")
    client2, addr2 = s.accept()

    print("Player 2 connected. Starting game")

    game = game.game()

    while True:


