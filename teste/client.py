import socket
import pickle
import message
import threading

class ClientThread(threading.Thread):
    def __init__(self, conn, playerId, daemon: bool | None = None) -> None:
        super().__init__(daemon=daemon)
        self.id = playerId
        self.conn_sock = conn
    
    def run(self):
        
        data = pickle.loads(self.conn_sock.recv(1024))
        print(data.code)
        if data.code == 0:
            print("Waiting for opponent")
            data = self.conn_sock.recv(1024)
            print("FODASE A PORRA DA MENSAGEM DO IF CODE.CODE == 0!")

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
        while True:
            
            data = pickle.loads(self.conn_sock.recv(1024))  # Recebe dados do servidor
            
            if data.code == 2:
                print("###############################################\n" + data.message)
                print("Bullets: ", data.bullets)
                
                # Lógica para escolher a ação
                while True:
                    action = input("Enter your action: ")
                    if action not in ["DEFEND", "SHOOT", "RELOAD"]:
                        print("Invalid action")
                    elif action == "SHOOT" and data.bullets == 0:
                        print("You can only shoot if you have bullets.")
                    else:
                        break
                print("###############################################\n")
                self.conn_sock.sendall(pickle.dumps(message.message(2, action, "")))  # Envia ação ao servidor

            elif data.code == 1:
                print(data.message)
                print("\n###############################################\n")
                action = input("Enter your action: ")
                self.conn_sock.sendall(pickle.dumps(message.message(2, action, "")))

            elif data.code == 3:
                print(data.message)
                response = input("Do you want to play again? (y/n): ")
                
                if response == 'y':
                    self.conn_sock.sendall(pickle.dumps(message.message(1, "", "")))
                else:
                    self.conn_sock.sendall(pickle.dumps(message.message(3, "", "")))
                    data = pickle.loads(self.conn_sock.recv(1024))  # Recebe mais dados

                if data.code == 3:
                    print(data.message)
                    break
                else:
                    print("\n###############################################\n" + data.message)
                    action = input("Enter your action: ")
                    self.conn_sock.sendall(pickle.dumps(message.message(2, action, "")))
            else:
                print("Invalid message")
                break

# Função principal do cliente
def main():
    HOST = '127.0.0.1'  # Endereço do servidor
    PORT = 65432  # Porta do servidor

    try:
        # Cria o socket e conecta ao servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))  # Conecta ao servidor
            print("Conectado ao servidor!")

            # Inicializa a thread do cliente
            client_thread = ClientThread(s, playerId=1)  # Define o ID do jogador
            client_thread.start()  # Inicia a thread de comunicação

            # Espera a thread finalizar
            client_thread.join()

    except Exception as e:
        print(f"Erro ao conectar: {e}")

if __name__ == "__main__":
    main()
