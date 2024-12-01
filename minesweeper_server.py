import socket
import random
from threading import Thread
import json
import time

class MinesweeperServer:
    def __init__(self, host="0.0.0.0", port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)

        self.clients = []
        self.board = None
        self.game_started = False

    def generate_board(self, size_x=10, size_y=10):
        # To generate a consistent board for both players
        random.seed(time.time())
        board = []
        mines = 0

        for x in range(size_x):
            row = []
            for y in range(size_y):
                is_mine = random.random() < 0.1
                if is_mine:
                    mines += 1
                    
                row.append({
                    'isMine': is_mine,
                    "mines": 0,
                    'state': 0
                })
            board.append(row)

        for x in range(size_x):
            for y in range(size_y):
                nearby_mines = self.count_mines(board, x, y)
                board[x][y]['mines'] = nearby_mines
        
        return board, mines
    
    def count_mines(self, board, x, y):
        size_x, size_y = len(board), len(board[0]) # 10
        mine_count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size_x and 0 <= ny < size_y and board[nx][ny]['isMine']:
                    mine_count += 1
                
        return mine_count
    
    def handle_client(self, client_socket, client_id):
        try:
            board_data = json.dumps({
                'board': self.board,
                'mines': self.mines,
                'client_id': client_id
            })

            client_socket.send(board_data.encode())

            while True:
                # Receieve moves from client
                data = client_socket.recv(4096).decode()
                if not data:
                    break

                move = json.loads(data)

                for other_client in self.clients:
                    if other_client != client_socket:
                        other_client.send(json.dumps(move).encde())

        except Exception as e:
            print(f"Client {client_id} disconnected: {e}")
        finally:
            client_socket.close()
            self.clients.remove(client_socket)

    def start(self):
        print(f"Server is listening on {self.host}:{self.port}")

        self.board, self.mines = self.generate_board()
        while len(self.clients) < 2:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address}")
            self.clients.append(client_socket)

            client_id = len(self.clients)
            client_thread = Thread(
                target=self.handle_client,
                args=(client_socket, client_id)
            )
            client_thread.start()

        self.game_started = True

        print("Game start")

def main():
    server = MinesweeperServer()
    server.start()


if __name__ == "__main__":
    main()