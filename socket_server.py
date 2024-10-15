import os
import socket
from datetime import datetime

class SocketServer:
    def __init__(self):
        self.bufsize = 1024
        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read()

        self.DIR_PATH = './request'
        self.createDir(self.DIR_PATH)

    def createDir(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")

    def run(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        print("Start the socket server...")
        print("\"Ctrl+C\" for stopping the server!\r\n")

        try:
            while True:
                clnt_sock, req_addr = self.sock.accept()
                clnt_sock.settimeout(5.0)
                print("Request message...\r\n")

                response = b""

                try:
                    while (chunk := clnt_sock.recv(self.bufsize)):
                        response += chunk
                except socket.timeout:
                    print("Socket timeout...\r\n")

                if response:
                    time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    name = f'{self.DIR_PATH}/{time}.bin'
                    with open(name, 'wb') as file:
                        file.write(response)

                clnt_sock.sendall(self.RESPONSE)

                clnt_sock.close()
        except KeyboardInterrupt:
            print("\r\nStop the server...")

        self.sock.close()

if __name__ == "__main__":
    server = SocketServer()
    server.run("127.0.0.1", 8000)
