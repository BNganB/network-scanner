#!/bin/python3

import sys
import socket
import threading
from datetime import datetime
import re


PORT_RANGE_MIN = 0
PORT_RANGE_MAX = 1023

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:  # 0 = open, 1 = closed
            print(f"Port {port} is open")
        s.close()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()
    except socket.error:
        print("Could not connect to the server")
        sys.exit()

def is_valid_ip(ip_str):
    valid_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(valid_pattern, ip_str) is not None

def main():
    if len(sys.argv) != 2:
        print("Invalid amount of arguments\nSyntax: python3 scanner.py <ip>")
        sys.exit()

    ip_address = sys.argv[1]

    target = socket.gethostbyname(ip_address)
    

    # BROKEN, gets wrong ipaddress, FIX ASAP
    """if not is_valid_ip(target):
        target = socket.gethostbyname(socket.gethostname())
        print(f"Invalid IP address syntax, defaulting to {target}")"""
        

    print("-" * 50)
    print(f"Scanning target {target}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)

    try:
        threads = []
        for port in range(PORT_RANGE_MIN, PORT_RANGE_MAX + 1):
            thread = threading.Thread(target=scan_port, args=(target, port))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()

if __name__ == "__main__":
    main()
