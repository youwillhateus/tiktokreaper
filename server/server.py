"""

C2C (Command and Control) Server for monitoring and controling bots or any other modules

"""

import socket
import threading

class C2C(object):
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0", 65533))
        self.server.listen()
    
    def update(self) -> None:
        """Sends information such as how many bots are connected, how many proxies are available to each user connected to the C2"""
        while True:
            return

    def handle(self, sock: socket.socket, addr: tuple) -> None:
        while True:
            try:
                data = sock.recv(1024)

                if not data: raise 
    
            except:
                return sock.close()

    def main(self) -> None:
        threading.Thread(target = self.update).start()
        print("[+] Listening...")

        while True:
            sock, addr = self.server.accept()
            threading.Thread(target = self.handle, args = (sock, addr)).start()