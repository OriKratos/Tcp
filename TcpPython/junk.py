from TCPClient.TCPClient import TCPClient
from Kratos.KratosProtocol import KratosProtocol
from Kratos.CommandList import CommandList
import logging
from prettytable import PrettyTable
from rich.console import Console
client = TCPClient(host="10.0.1.3", port=5555)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# ANSI escape codes for colors
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

# Create a PrettyTable
Pbittable = PrettyTable()
Pbittable.field_names = ["Testname", "Pass/Fail"]

# Add rows dynamically with color
rows = [
    ["Temperature ACPI", "Pass"],
    ["Temperature ISA", "Fail"],
    ["Temperature Core 0", "Pass"]
]

for row in rows:
    status = row[1]
    colored_status = f"{GREEN}Pass{RESET}" if status == "Pass" else f"{RED}Fail{RESET}"
    Pbittable.add_row([row[0], colored_status])

# Add horizontal lines between rows
Pbittable.hrules = 1  # Applies horizontal lines after each row

# Print the table using logging
logging.info("\n" + str(Pbittable))
command=CommandList
