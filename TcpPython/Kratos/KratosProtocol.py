from TCPClient import TCPClient
import logging
from prettytable import PrettyTable


class KratosProtocol:
    logger=logging.getLogger("KratosProtocol")
    logger.setLevel(logging.DEBUG)
    formatter=logging.Formatter('%(levelname)s  %(message)s')

    def __init__(self, client: TCPClient):
        """
        Initialize the KratosProtocol with a TCPClient instance.
        :param client: An instance of TCPClient.
        """
        self.client = client 
        
    def calculate_checksum(self, preamble: int, command: int, dataLength: int, data: bytes) -> int:
    # Convert all fields to bytes and concatenate them
        buffer = ( #array[]
        preamble.to_bytes(2, 'little') +
        command.to_bytes(2, 'little') +
        dataLength.to_bytes(4, 'little') +
        data
    )
        checksum = sum(buffer) & 0xFFFF  #מחבר את הערכים של בופר ומשאיר רק 16 סיביות 
        return checksum

    def send_frame(self, frame: dict): 
        if "checksum" not in frame:
            if frame["dataLength"] > 0:
                if not isinstance(frame["data"], bytes): #check if data in bytes
                    raise ValueError("frame['data'] must be of type 'bytes'")
                if len(frame["data"]) != frame["dataLength"]:
                    raise ValueError(f"Data length mismatch: Expected {frame['dataLength']} bytes, but got {len(frame['data'])} bytes.")

        frame["checksum"] = self.calculate_checksum(
            frame["preamble"],
            frame["command"],
            frame["dataLength"],
            frame["data"]
        )

    # Construct the frame bytes
        frame_bytes = ( #מבנה אחיד 
            frame["preamble"].to_bytes(2, 'little') +
            frame["command"].to_bytes(2, 'little') +
            frame["dataLength"].to_bytes(4, 'little') +
            frame["data"] +
            frame["checksum"].to_bytes(2, 'little')
        )

        logging.debug(f"Debug: Print the frame being sent DEBUG: Sending frame: {frame_bytes.hex()}")

    # Send the frame
        self.client.send_data(frame_bytes)

    def receive_frame(self) -> dict:
        """
        Receive a frame using the Kratos protocol.
        :return: A dictionary representing the frame structure.
        """
        # Read the header (8 bytes: preamble, command, dataLength)
        header_size = 8
        header_data = self.client.receive_data(header_size)
        if len(header_data) < header_size:
            raise ValueError("Failed to read the full header.")

        preamble = int.from_bytes(header_data[0:2], 'little')
        command = int.from_bytes(header_data[2:4], 'little')
        data_length = int.from_bytes(header_data[4:8], 'little')

        # Read the data (dataLength bytes)
        data = self.client.receive_data(data_length)
        if len(data) < data_length:
            logging.error(f"Failed to read all data bytes. Expected: {data_length}, Received: {len(data)}")


        # Read the checksum (2 bytes)
        checksum_data = self.client.receive_data(2)
        if len(checksum_data) < 2:
            self.logger.error(f"Failed to read all data bytes. Expected: {data_length}, Received: {len(data)}")

        received_checksum = int.from_bytes(checksum_data, 'little')

        logging.debug(f"Print the received frame parts ,DEBUG: Received frame parts - "
            f"preamble: {hex(preamble)}, command: {hex(command)}, "
            f"data_length: {data_length}, checksum: {hex(received_checksum)}")

        # Verify the checksum
        calculated_checksum = self.calculate_checksum(
        preamble=int.from_bytes(header_data[0:2], 'little'),
        command=int.from_bytes(header_data[2:4], 'little'),
        dataLength=int.from_bytes(header_data[4:6], 'little'),
        data=data
)

    
        return {
            "preamble": preamble,
            "command": command,
            "dataLength": data_length,
            "data": data,
            "checksum": received_checksum
        }

        
