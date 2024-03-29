#!/bin/python3

import sys
import socket
import threading
import time
import re
import os


PORT_RANGE_MIN = 0
PORT_RANGE_MAX = 1023
open_ports = []
timer = time.strftime("%Y%m%d-%H%M%S")

def save_to_file(ip, date, ports):
    if not os.path.exists(os.path.join(os.getcwd(), "logs")):
        os.mkdir("logs")
    with open(f"logs/{timer} log.txt", "x") as f:
        f.write(f"{date}\n{ip}\n\n")
        for port in ports:
            f.write(f"{port} is open\n")
        f.write("EOF")
    print("Log saved!")



def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:  # 0 = open, 1 = closed
            print(f"Port {port} is open")
            open_ports.append(port)
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
        print("Invalid amount of arguments\nSyntax: python3 socket-scanner.py <ip>")
        sys.exit()

    ip_address = sys.argv[1]

    target = socket.gethostbyname(ip_address)
    

    # BROKEN, gets wrong ipaddress, FIX ASAP
    """if not is_valid_ip(target):
        target = socket.gethostbyname(socket.gethostname())
        print(f"Invalid IP address syntax, defaulting to {target}")"""
        

    print("-" * 50)
    print(f"Scanning target {target}")
    print(f"Time started: {timer}")
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

    save_to_file(ip_address, timer, open_ports)

if __name__ == "__main__":
    main()
