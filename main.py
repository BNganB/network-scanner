from scapy.all import ARP, Ether, srp
import subprocess
import re
import requests
import json

# just use tty if on linux?
def get_ip_address():
    ipv4_pattern = r'IPv4 Address\. . . . . . . . . . . : (\d+\.\d+\.\d+\.\d+)'
    raw_output = subprocess.run("ipconfig", capture_output=True, text=True).stdout

    match = re.search(ipv4_pattern, raw_output)

    if match:
        ipv4_address = match.group(1)
        return ipv4_address
    else:
        return 1

# tty backup solution on linux
def get_ip_address_v2():
    ip = subprocess.run("tty", capture_output=True, text=True).stdout
    return int(ip)

def get_address_range(ip_address):
    cidr = input("Input custom CIDR (Default = /24, enter to continue):\n")
    if cidr in (None, "", "n", "no", "No", "skip"):
        cidr = "/24"
    if cidr.startswith("/"):
        return ip_address + cidr
    else:
        return (f"{ip_address}/{cidr}")
    

def calc_subset_mask(ip_address):
    cidr = int(ip_address[-2] + ip_address[-1])
    # if this doesn't work for other test cases (single digit range), use find (kinda bad tho)
    # index_of_slash = ip_address.find("/")
    # cidr = ip_address[index_of_slash + 1]
    cidr_to_bits = 32 - cidr

    binary_subset_mask = "1" * cidr_to_bits + "0" * (32 - cidr_to_bits)

    subnet_mask = '.'.join([str(int(binary_subset_mask[i:i+8], 2)) for i in range(0, 32, 8)])

    return subnet_mask



def create_ARP_packet(ip_address):
    arp = ARP(pdst=ip_address)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp  # combine ether+arp
    return packet


def send_packet(packet):
    result = srp(packet, timeout=3, verbose=0)[0]
    return result


def format_results(result, subnet_mask):
    print(f"Subnet mask - {subnet_mask}\nDevices in the network:")
    for sent, received in result:
        mac_address = received.hwsrc
        # so ugly maybe take api request into another function?
        r = requests.get(
            f"https://www.macvendorlookup.com/api/v2/{mac_address}")
        data_list = json.loads(r.text)
        company_value = data_list[0]["company"]
        # nice new trick, can use != for inverse case
        if company_value in ("", None):
            company_value = "Unsure"
        print(
            f"IP: {received.psrc} - MAC: {received.hwsrc} - Vendor: {company_value}")


if __name__ == "__main__":
    ip = get_ip_address()
    if ip == 1:
        print("Cannot get ip from cmd");exit()
    else:
        ip = get_address_range(ip)
        packet = create_ARP_packet(ip)
        # SYN > SYN ACK > ACK
        result = send_packet(packet)
        subset_mask = calc_subset_mask(ip)
        format_results(result, subset_mask)
