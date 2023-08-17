import subprocess


ipv4_pattern = r'IPv4 Address\. . . . . . . . . . . : (\d+\.\d+\.\d+\.\d+)'
raw_output = subprocess.run("ifconfig", capture_output=True, text=True).stdout

match = re.search(ipv4_pattern, raw_output)

if match:
    ipv4_address = match.group(1)
    return ipv4_address
else:
    return 1