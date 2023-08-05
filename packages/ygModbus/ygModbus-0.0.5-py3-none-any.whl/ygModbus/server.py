#!/usr/bin/env python3

"""
Modbus/TCP server with start/stop schedule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run this as root to listen on TCP privileged ports (<= 1024).

Default Modbus/TCP port is 502, so we prefix call with sudo. With argument
"--host 0.0.0.0", the server listens on all IPv4 interfaces of the host, instead of just
opening tcp/502 on the local interface.
$ sudo ./server_schedule.py --host 0.0.0.0
"""

import argparse
import json
import random
import signal
import sys
import time
from datetime import datetime
from pyModbusTCP.server import ModbusServer, DataBank
import schedule


class MyDataBank(DataBank):
    """A custom ModbusServerDataBank for overriding the get_holding_registers method."""

    def __init__(self, register_params):
        # Turn off allocation of memory for standard Modbus object types.
        # Only "holding registers" space will be replaced by dynamically built values.
        super().__init__(virtual_mode=True)
        self.register_params = register_params
        self.latest_data = {}

    def update_holding_registers(self):
        """Update the holding registers with random values based on the given parameters."""
        for address, params in self.register_params.items():
            self.latest_data[address] = random.randint(params['min_int'], params['max_int'])
        self.set_holding_registers(0, list(self.latest_data.values()))

    def get_holding_registers(self, address, number=1, srv_info=None):
        """Get the latest values of holding registers."""
        try:
            print(self.latest_data)
            return [self.latest_data.get(str(a), 0) for a in range(address, address + number)]
        except KeyError:
            return

def run_server():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='127.0.0.1', help='Host (default: 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, default=502, help='TCP port (default: 502)')
    parser.add_argument('-j', '--json', type=str, default='register_params.json', help='JSON file with register parameters (default: register_params.json)')
    parser.add_argument('-i', '--interval', type=float, default=1.0, help='Interval in seconds for updating holding registers (default: 1.0)')
    args = parser.parse_args()

    # Load register parameters from JSON file
    try:
        with open(args.json) as json_file:
            register_params = json.load(json_file)
    except FileNotFoundError:
        print(f'Error: JSON file "{args.json}" not found.')
        return
    except json.JSONDecodeError:
        print(f'Error: Invalid JSON format in "{args.json}".')
        return

    # Initialize Modbus server and start it
    server = ModbusServer(host=args.host, port=args.port, no_block=True, data_bank=MyDataBank(register_params))
    server.start()
    print('Modbus TCP server is running on', args.host)

    def terminate_server(signal, frame):
        """Handler for terminating the server gracefully."""
        print('\nTerminating server...')
        server.stop()
        sys.exit(0)

    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, terminate_server)

    def update_holding_registers():
        """Update the holding registers with random values based on the given parameters."""
        server.data_bank.update_holding_registers()

    # Schedule the update of holding registers at the specified interval
    schedule.every(args.interval).seconds.do(update_holding_registers)

    # Main loop
    while True:
        schedule.run_pending()
        time.sleep(0.1)


# if __name__ == "__main__":
#     run_server()

# run_server()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(prog="ygModbus")
#     subparsers = parser.add_subparsers(dest="command")

#     runserver_parser = subparsers.add_parser("runserver", help="Run the server")

#     args = parser.parse_args()

#     if args.command == "runserver":
#         run_server()


