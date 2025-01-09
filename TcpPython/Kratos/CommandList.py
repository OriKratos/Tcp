from Kratos.KratosProtocol import KratosProtocol
import logging
from prettytable import PrettyTable

class CommandList:
    logger=logging.getLogger("CommandList")
    logger.setLevel(logging.DEBUG)
    formatter=logging.Formatter('%(levelname)s  %(message)s')
    def __init__(self):
        self=self
    def getSwVerSBC(protocol: KratosProtocol):
        frame = {
            "preamble": 0x0054,
            "command": 0x101,
            "dataLength": 0,
            "data": b''
        } 
        protocol.send_frame(frame)
        response_frame = protocol.receive_frame()
        logging.info("SBC VER V" + str((response_frame["data"][0])) + "." +
            str(response_frame["data"][1]) + " Date : " +
            str(response_frame["data"][2]) + "/" +
            str(response_frame["data"][3]) + "/" +
            str(int.from_bytes(response_frame["data"][4:6], byteorder="little")))


    def getSwVerMCU(protocol: KratosProtocol):
        frame = {
            "preamble": 0x0054,
            "command": 0x201,
            "dataLength": 0,
            "data": b''
        } 
        protocol.send_frame(frame)
        response_frame = protocol.receive_frame()
        logging.info("MCU VER V" + str((response_frame["data"][0])) + "." +
            str(response_frame["data"][1]) + " Date : " +
            str(response_frame["data"][2]) + "/" +
            str(response_frame["data"][3]) + "/" +
            str(int.from_bytes(response_frame["data"][4:6], byteorder="little")))


    def getSwVerRPU(protocol: KratosProtocol):
        frame = {
            "preamble": 0x0054,
            "command": 0x301,
            "dataLength": 0,
            "data": b''
        }
        protocol.send_frame(frame)
        response_frame = protocol.receive_frame()
        logging.info("FPGA VER V" + str((response_frame["data"][0])) + "." +
            str(response_frame["data"][1]) + " Date : " +
            str(response_frame["data"][2]) + "/" +
            str(response_frame["data"][3]) + "/" +
            str(int.from_bytes(response_frame["data"][4:6], byteorder="little")))
        logging.info("RPU SW VER V" + str((response_frame["data"][6])) + "." +
            str(response_frame["data"][7]) + " Date : " +
            str(response_frame["data"][8]) + "/" +
            str(response_frame["data"][9]) + "/" +
            str(int.from_bytes(response_frame["data"][10:12], byteorder="little")))
        logging.info("APU SW VER V" + str((response_frame["data"][12])) + "." +
            str(response_frame["data"][13]) + " Date : " +
            str(response_frame["data"][14]) + "/" +
            str(response_frame["data"][15]) + "/" +
            str(int.from_bytes(response_frame["data"][16:18], byteorder="little")))
        logging.info("RFSoM HW VER V" + str((response_frame["data"][24])) + "." +
            str(response_frame["data"][25]) + " Serial number LSB : " +
            str(response_frame["data"][26]) + " Serial Number MSB : " +
            str(response_frame["data"][21]) + " RFFE HW Ver : " +
            str(int.from_bytes(response_frame["data"][22:24], byteorder="little")))  
        
    def _status_passfail(frame, num_byte, bit):
            """
            Private function to determine "Pass" or "Fail" based on a specific bit in a specific byte of `frame["data"]`.
            Args:
                frame (dict): The frame dictionary containing "data".
                num_byte (int): The byte index to evaluate.
                bit (int): The bit position (0-7) to evaluate in the selected byte.
            Returns:
                str: "Pass" if the bit is 1, "Fail" if the bit is 0.
            """
            if num_byte >= len(frame["data"]):
                raise ValueError(f"Byte index {num_byte} is out of range for the data field.")
            if not (0 <= bit <= 7):
                raise ValueError(f"Bit position {bit} must be between 0 and 7.")
            return "Pass" if (frame["data"][num_byte] >> bit) & 1 else "Fail"
    
    def getPbitStatus(protocol: KratosProtocol):
        frame = {
            "preamble": 0x0054,
            "command": 0x102,
            "dataLength": 0,
            "data": b''
        }

        protocol.send_frame(frame)
        response_frame = protocol.receive_frame()


        # Create a table
        Pbittable = PrettyTable()
        Pbittable.field_names = ["Testname", "Pass/Fail"]

        # Add rows dynamically
        Pbittable.add_row(["Temperature ACPI",CommandList._status_passfail(response_frame,0,7)])
        Pbittable.add_row(["Temperature  ISA", CommandList._status_passfail(response_frame,0,6)])
        Pbittable.add_row(["Temperature Core 0", CommandList._status_passfail(response_frame,0,5)])
        Pbittable.add_row(["Temperature Core 1", CommandList._status_passfail(response_frame,0,4)])
        Pbittable.add_row(["Temperature Core 2", CommandList._status_passfail(response_frame,0,3)])
        Pbittable.add_row(["Temperature Core 3", CommandList._status_passfail(response_frame,0,2)])
        Pbittable.add_row(["P5V", CommandList._status_passfail(response_frame,0,1)])
        Pbittable.add_row(["P12V", CommandList._status_passfail(response_frame,0,0)])
        Pbittable.add_row(["P3V Battery", CommandList._status_passfail(response_frame,1,7)])
        Pbittable.add_row(["Ethernet Communication", CommandList._status_passfail(response_frame, 1, 6)])
        Pbittable.add_row(["USB3 Communication", CommandList._status_passfail(response_frame, 1, 5)])
        Pbittable.add_row(["SE050 Security Element Communication", CommandList._status_passfail(response_frame, 1, 4)])
        Pbittable.add_row(["DDR4 memory 16GB", CommandList._status_passfail(response_frame, 1, 3)])
        Pbittable.add_row(["PCIE CARD Communication", CommandList._status_passfail(response_frame, 1, 2)])
        Pbittable.add_row(["STORAGE HEALTH", CommandList._status_passfail(response_frame, 1, 1)])
        Pbittable.add_row(["Spare 0", CommandList._status_passfail(response_frame, 1, 0)])

        # Add horizontal lines between rows
        Pbittable.hrules = 1  # Applies horizontal lines after each row

        # Print the table
        logging.info("\n" + str(Pbittable))

    def calculate_temperature(frame,num_byte):
            value = (frame["data"][num_byte+1] << 8) | frame["data"][num_byte]

            if value > 32767:
                value -= 65536
            temperature = (value / 100) - 50
            formatted_number = f"{temperature:.2f}"
            return(formatted_number)
    
    def calculate_volt(frame,num_byte):
            value = (frame["data"][num_byte+1] << 8) | frame["data"][num_byte]

            if value > 32767:
                value -= 65536
            volt = (value / 100)
            formatted_number = f"{volt:.2f}"
            return(formatted_number)
    
    def read_bit_param(protocol:KratosProtocol):
        frame = {
            "preamble": 0x0054,
            "command": 0x103,
            "dataLength": 0,
            "data": b''
        }
        protocol.send_frame(frame)
        response_frame = protocol.receive_frame()
        bittable = PrettyTable()
        bittable.field_names = ["Testname", "Parameters"]
        bittable.add_row(["Temperature ACPI", f"{CommandList.calculate_temperature(response_frame, 0)} *C"])
        bittable.add_row(["Temperature ISA", f"{CommandList.calculate_temperature(response_frame, 2)} *C"])
        bittable.add_row(["Temperature Core 0", f"{CommandList.calculate_temperature(response_frame, 4)} *C"])
        bittable.add_row(["Temperature Core 1", f"{CommandList.calculate_temperature(response_frame, 6)} *C"])
        bittable.add_row(["Temperature Core 2", f"{CommandList.calculate_temperature(response_frame, 8)} *C"])
        bittable.add_row(["Temperature Core 3", f"{CommandList.calculate_temperature(response_frame, 10)} *C"])
        bittable.add_row(["P5V", f"{CommandList.calculate_volt(response_frame, 12)} V"])
        bittable.add_row(["P12V", f"{CommandList.calculate_volt(response_frame, 14)} V"])
        bittable.add_row(["P3V Battery", f"{CommandList.calculate_volt(response_frame, 16)} V"])

        bittable.hrules = 1  

        logging.info("\n" + str(bittable))
    def getCbitStatus(protocol: KratosProtocol):
        frame = {
            "preamble": 0x0054,
            "command": 0x104,
            "dataLength": 0,
            "data": b''
        }

        protocol.send_frame(frame)
        response_frame = protocol.receive_frame()


        # Create a table
        Pbittable = PrettyTable()
        Pbittable.field_names = ["Testname", "Pass/Fail"]

        logging.info("Cbit Status:")
        Pbittable.add_row(["Temperature ACPI",CommandList._status_passfail(response_frame,0,7)])
        Pbittable.add_row(["Temperature  ISA", CommandList._status_passfail(response_frame,0,6)])
        Pbittable.add_row(["Temperature Core 0", CommandList._status_passfail(response_frame,0,5)])
        Pbittable.add_row(["Temperature Core 1", CommandList._status_passfail(response_frame,0,4)])
        Pbittable.add_row(["Temperature Core 2", CommandList._status_passfail(response_frame,0,3)])
        Pbittable.add_row(["Temperature Core 3", CommandList._status_passfail(response_frame,0,2)])
        Pbittable.add_row(["P5V", CommandList._status_passfail(response_frame,0,1)])
        Pbittable.add_row(["P12V", CommandList._status_passfail(response_frame,0,0)])
        Pbittable.add_row(["P3V Battery", CommandList._status_passfail(response_frame,1,7)])
        Pbittable.add_row(["Ethernet Communication", CommandList._status_passfail(response_frame, 1, 6)])
        Pbittable.add_row(["USB3 Communication", CommandList._status_passfail(response_frame, 1, 5)])
        Pbittable.add_row(["SE050 Security Element Communication", CommandList._status_passfail(response_frame, 1, 4)])
        Pbittable.add_row(["DDR4 memory 16GB", CommandList._status_passfail(response_frame, 1, 3)])
        Pbittable.add_row(["PCIE CARD Communication", CommandList._status_passfail(response_frame, 1, 2)])
        Pbittable.add_row(["STORAGE HEALTH", CommandList._status_passfail(response_frame, 1, 1)])
        Pbittable.add_row(["Spare 0", CommandList._status_passfail(response_frame, 1, 0)])

        # Add horizontal lines between rows
        Pbittable.hrules = 1  # Applies horizontal lines after each row

        # Print the table
        logging.info("\n" + str(Pbittable))

