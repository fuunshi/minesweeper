from threading import Thread

import socket
import json
import tkinter as tk

class MultiplayerMinesweeper:
    def __init__(self, host="0.0.0.0", port=5555):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        self.root = tk.Tk()
        self.root.title("Multiplayer")

        self.board = None
        self.mines = 0
        self.client_id = None
        self.buttons = {}

        self.setup_ui()

        recieve_thread = Thread(target=self.recieve_updates)
        recieve_thread.daemon = True
        recieve_thread.start()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self,status_label = tk.Label(
            self.root,
            text = "waiting for game to start",
            font = ("Arial", 12)


        )
        self.status_label.pack()

    def recieve_updates(self):
        try:
            data =self.client_socket.recv(4096).decode()
            game_data = json.loads(data)

            self.board = game_data['board']
            self.mines = game_data['miines']
            self.client_id = game_data['client_id']

            self.root.after(0, self.create_board)

            while True:
                move_data = self.client_socket.recv(4096).decode()
                move = json.loads(move_data)
                self.root.after(0, self.process_opponent_move, move)

        except Exception as e:
            tk.messagebox.showerror("connection Lost")

    def create_board(self):
        self.status_label.config(
            text = f"Player {self.client_id} - Mines: {self.mines}"
        )
        pass

    def create_board(self):
        pass

    def on_click(self):
        pass

    def process_opponent_move(self):
        pass

    def update_tile(self):
        pass    

    def run(self):
        self.root.mainloop()

def main():
    game = MultiplayerMinesweeper()
    game.run()

if __name__ == "__main__":
    main()
