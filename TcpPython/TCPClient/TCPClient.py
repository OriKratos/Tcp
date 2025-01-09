import socket
import logging

class TCPClient:
    logger=logging.getLogger("KratosProtocol")
    logger.setLevel(logging.DEBUG)
    formatter=logging.Formatter('%(levelname)s  %(message)s')

    def __init__(self, host: str, port: int):
        
        self.host = host
        self.port = port
        self.client_socket = None  

    def connect(self):
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        logging.debug(f"Connected to {self.host}:{self.port}")

    def send_data(self, data: bytes) -> int:
        if self.client_socket is None:
            logging.error("Socket is not connected. Attempted to send data without calling connect().")
            raise ConnectionError("Socket is not connected. Call connect() first.")
        
        self.client_socket.sendall(data)
        return len(data)

    def receive_data(self, buffer_size: int) -> bytes:
        
        if self.client_socket is None:
            raise ConnectionError("Socket is not connected. Call connect() first.")
        
        return self.client_socket.recv(buffer_size)

    def close(self):
        
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            logging.info("Connection closed.")
