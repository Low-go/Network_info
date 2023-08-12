import subprocess
import re
import nmap


def find_default_gateway():
    # Run the "ipconfig" command in CMD and capture the output
    cmd_output = subprocess.check_output("ipconfig", shell=True, text=True)

    # Split the output into lines
    lines = cmd_output.splitlines()

    # Search for the line containing "Default Gateway"
    for line in lines:
        if "Default Gateway" in line:
            # Use regular expression to find numbers
            numbers = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
            return numbers[0] if numbers else "Default Gateway not found"

    return "Default Gateway not found"

def find_subnet_mask():
    cmd_output = subprocess.check_output("ipconfig", shell=True, text=True)

    # Split the output into lines
    lines = cmd_output.splitlines()

    for line in lines:
        if "Subnet Mask" in line:
            numbers = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
            return numbers[0] if numbers else "Subnet Mask not found"

    return "Subnet mask not found"

def convert_Subnet(mask):
    hold_mask = mask.split('.')
    mid_mask = ""
    new_mask = 0


    for i in hold_mask:
        mid_mask += bin(int(i))[2:]

    for i in mid_mask:
        if i == '1':
            new_mask += 1


    return str(new_mask)


default_gateway_ip = find_default_gateway()
#retrieves default gateway from cmd
#print(default_gateway_ip)

subnet_mask = find_subnet_mask()
convert = convert_Subnet(subnet_mask)
#print(convert)


class Network(object):
    def __init__(self):
        self.ip = default_gateway_ip
        self.mask = convert

    def networkscanner(self):
        network = self.ip + '/' + self.mask

        nm = nmap.PortScanner()
        nm.scan(hosts = network, arguments='-sn')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for host, status in hosts_list:
            print("Host\t{}".format(host))


if __name__ == '__main__':
    N = Network()
    N.networkscanner()



