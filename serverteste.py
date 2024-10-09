import socket, pickle
import game
import message

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


#def PlayersLoop(connec, playerId):



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:


    s.bind((HOST, PORT))
    s.listen(2)
    print("Waiting for players to connect")
    client1, addr1 = s.accept()
    print(client1)
    client1.sendall(pickle.dumps(message.message(0, "", "")))
    print("Player 1 connected. Waiting for player 2 to connect")
    client2, addr2 = s.accept()
    print(client2)
    client1.sendall(pickle.dumps(message.message(1, "", "")))
    client2.sendall(pickle.dumps(message.message(1, "", "")))
    print("Player 2 connected. Starting game")

    game = game.game()

    messagePack = message.message(2, "", "Primeira ação")
    messagePack.bullets = game.p1Bullets
    client1.sendall(pickle.dumps(messagePack))
    client2.sendall(pickle.dumps(messagePack))

    while True:
        #TODO: consertar a ordem dos players
        # depois de conectar aos clientes, fazer 1 thread pra cada: Thread1 = threading.Thread(target=playerLoop, args=(conn1,#id do player)).start() 
        # conn1 (é um socket) veio de: conn1, addr1 = server_socket.accept()
        data = pickle.loads(client1.recv(1024))
        data2 = pickle.loads(client2.recv(1024))
        if data.code == 2 and data2.code == 2:
            result = game.action(data.action, data2.action)
            if result.isnumeric():
                if result == '1':
                    messagePack = message.message(result, "", f"A rodada acabou. Pontuação: Player 1 ({game.p1Points} x {game.p2Points}) Player 2\nRodadas restantes: {game.rounds}")
                else:
                    messagePack = message.message(result, "", f"O jogo acabou. Pontuação final: Player 1 ({game.p1Games} x {game.p2Games}) Player 2\nDo you want to play again? (y/n)")	
                client1.sendall(pickle.dumps(messagePack))
                client2.sendall(pickle.dumps(messagePack))
            else:
                messagePack = message.message(2, "", result)
                messagePack.bullets = game.p1Bullets
                client1.sendall(pickle.dumps(messagePack))
                messagePack.bullets = game.p2Bullets
                client2.sendall(pickle.dumps(messagePack))
        elif data.code == 3 or data2.code == 3:
            print(data.message)
            print(data2.message)
            break
        else:
            print("Invalid message")
            break


