import socket, pickle 
import game
import message
import threading

#HOST = "192.168.15.9"
#HOST = "192.168.15.85"
HOST = "127.0.0.1"  # Endereço de interface de loopback padrão (localhost)
PORT = 65432  # Porta para escutar (portas não privilegiadas são > 1023)
 
# Função para lidar com o chat
def handle_chat(conn, player_id, chats):
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(f"Player {player_id} sent: {message}")
            transmit_message(f"Player {player_id}: {message}", conn, chats)
        except:
            break

# Função para transmitir mensagens de chat para o outro jogador
def transmit_message(message, conn, chats):
    for client in chats:
        if client != conn:
            print(f"Sending message to {client}")
            try:
                client.send(message.encode())
            except:
                continue

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:


    s.bind((HOST, PORT))
    s.listen(4)
    print("Waiting for players to connect")
    client1, addr1 = s.accept()
    chat1, addrChat1 = s.accept()
    client1.sendall(pickle.dumps(message.message(0, "", "")))
    print("Player 1 connected. Waiting for player 2 to connect")
    client2, addr2 = s.accept()
    chat2, addrChat2 = s.accept()
    client1.sendall(pickle.dumps(message.message(1, "", "")))
    client2.sendall(pickle.dumps(message.message(1, "", "")))
    print("Player 2 connected. Starting game")

    chats = [chat1, chat2]
    
    threading.Thread(target=handle_chat, args=(chat1, 1, chats)).start()
    threading.Thread(target=handle_chat, args=(chat2, 2, chats)).start()
    
    print("Client 1 " + client1.recv(1024).decode("utf-8"))
    print("Client 2 " + client2.recv(1024).decode("utf-8"))

    game = game.game()

    messagePack = message.message(2, "", "First action\nYou are player 1")
    messagePack.bullets = game.p1Bullets
    client1.sendall(pickle.dumps(messagePack))
    messagePack.message = "First action\nYou are player 2"
    client2.sendall(pickle.dumps(messagePack))


    clients = [client1, client2]
    
    while True:
        
        data = pickle.loads(client1.recv(1024))
        data2 = pickle.loads(client2.recv(1024))

        # Para cada resultado de uma ação existe um código diferente
        if data.code == 2 and data2.code == 2:
            result = game.action(data.action, data2.action)
            
            # Fim de round
            if result == 1:

                messagePack = message.message(result, "", f"The round is over. Score: Player 1 ({game.p1Points} x {game.p2Points}) Player 2\nRemaining rounds: {game.rounds}")
                client1.sendall(pickle.dumps(messagePack))
                client2.sendall(pickle.dumps(messagePack))    

            # Fim de jogo                 
            elif result == 3:

                messagePack = message.message(result, "", f"{game.roundWinner} wins. The game is over. Overall final score: Player 1 ({game.p1Games} x {game.p2Games}) Player 2\nDo you want to play again? (y/n)")
                client1.sendall(pickle.dumps(messagePack))
                client2.sendall(pickle.dumps(messagePack))
                data = pickle.loads(client1.recv(1024))
                data2 = pickle.loads(client2.recv(1024))

                # Os dois jogadores querem jogar novamente
                if data.code == 1 and data2.code == 1:
                    messagePack = message.message(2, "", "First action")
                    messagePack.bullets = game.p1Bullets
                    client1.sendall(pickle.dumps(messagePack))
                    client2.sendall(pickle.dumps(messagePack))
                # Um dos jogadores não quer jogar novamente
                else:
                    messagePack = message.message(3, "", "One player doesn't want to play again")
                    client1.sendall(pickle.dumps(messagePack))
                    client2.sendall(pickle.dumps(messagePack))
                    break
            
            # Mensagem de ação
            elif result == 2:
                messagePack = message.message(2, "", f"Player 1 action: {data.action}, Player 2 action: {data2.action}\nPlayer 1 lives: {game.p1Lives}\nPlayer 2 lives: {game.p2Lives}")
                messagePack.bullets = game.p1Bullets
                client1.sendall(pickle.dumps(messagePack))
                messagePack.bullets = game.p2Bullets
                client2.sendall(pickle.dumps(messagePack))
            
            # Round empatado
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