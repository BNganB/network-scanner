from scapy.all import ARP, Ether, srp
import subprocess
import re
import requests
import json


def get_ip_address():
    ipv4_pattern = r'IPv4 Address\. . . . . . . . . . . : (\d+\.\d+\.\d+\.\d+)'
    raw_output = str(subprocess.run("ipconfig", capture_output=True))

    match = re.search(ipv4_pattern, raw_output)

    if match:
        ipv4_address = match.group(1)
        return ipv4_address + "/23"
    else:
        return 1


def create_ARP_packet(ip_address):
    arp = ARP(pdst=ip_address)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp  # combine ether+arp
    return packet


def send_packet(packet):
    result = srp(packet, timeout=3, verbose=0)[0]
    return result


def format_results(result):
    print("Devices in the network:")
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
        print("Cannot get ip from cmd")
        exit()
    else:
        packet = create_ARP_packet(ip)
        result = send_packet(packet)
        print(result)
        format_results(result)
