#!/bin/python3

import sys
import socket
from datetime import datetime

#Define target
if len(sys.argv) == 2: #argv = amount of arguments given
	target = socket.gethostbyname(sys.argv[1]) #Translate hostname to IPv4
else:
	printf("Invalid amount of arguments\nSyntax: python3 scanner.py <ip>")

print("-" * 50)
print(f"Scanning target {target}")
print(f"Time started: {datetime.now()}")
print("-" * 50)

try:
	for port in range(50, 85):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		result = s.connect_ex((target,port))
		if result == 0: #0 = open, 1 = closed
			print(f"Port {port} is open")
		s.close()
except KeyboardInterrupt:
	print("\nExiting...");sys.exit()
except socket.gaierror:
	print("Hostname could not be resolved.");sys.exit()
except socket.error:
	print("Could not connect to server");sys.exit()