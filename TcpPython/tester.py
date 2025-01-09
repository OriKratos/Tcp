from TCPClient.TCPClient import TCPClient
from Kratos.KratosProtocol import KratosProtocol
from Kratos.CommandList import CommandList
import logging
client = TCPClient(host="10.0.1.3", port=5555)


logger = logging.getLogger("TesterLogger")
logging.basicConfig(level=logging.INFO,
format='[%(asctime)s] [%(levelname)s] %(message)s',
datefmt='%H:%M:%S'
)
client.connect()
command = CommandList

# Initialize Kratos Protocol
protocol = KratosProtocol(client)

# Call functions from commandList
command.getSwVerSBC(protocol)
command.getSwVerMCU(protocol)
command.getSwVerRPU(protocol)
command.getPbitStatus(protocol)
command.read_bit_param(protocol)
command.getCbitStatus(protocol)
client.close()
