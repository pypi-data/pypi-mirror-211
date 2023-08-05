# import pandas as pd
import argparse
import datetime as dt
# import sqlalchemy
# from sqlalchemy import create_engine
from pyModbusTCP.client import ModbusClient

# c = ModbusClient(host="127.0.0.1", port=502, auto_open=True)
# regs = c.read_holding_registers(reg_addr=40001,reg_nb=4)
# regs

def request():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', type=str, default='127.0.0.1', help='Host (default: 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, default=502, help='TCP port (default: 502)')
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of holding registers (default: 1)')
    parser.add_argument('-s', '--start', type=int, default=40001, help='Starting register address (default: 40001)')
    args = parser.parse_args()
    
    c = ModbusClient(host=args.host, port=args.port, auto_open=True)
    regs = c.read_holding_registers(reg_addr=args.start, reg_nb=args.number)
    print(regs)
