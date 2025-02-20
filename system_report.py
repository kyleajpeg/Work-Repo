#!/usr/bin/env python3

# Name
# Date

# chmod +x system_report.py

import subprocess
import os
import time
import platform
import ipaddress


# Need to add more comments
#LINE UP ALL OUTPUT ! ! ! ----------------------- (also header)

"""
To do list:
Fix the spacing of output -> line up everything (and header) by copying and pasteing side by side
implement output to log file
double check sufficient comments
double check functions and requirements
ask AI to check as well ^

"""

RED = '\033[38;5;196m'
GREEN = '\033[38;5;46m'
RESET = '\033[0m'

def clear_screen(): # Better readability
    os.system('clear') # clears terminal

def create_header(): # Creates the header for the script and displays the date
    months = {'Jan': "January", 
              'Feb': "February",
              'Mar': "March",
              'Apr': "April",
              'May': "May",
              'Jun': "June",
              'Jul': "July",
              'Aug': "August",
              'Sep': "September",
              'Nov': "November",
              'Dec': "December"
    }
    result = subprocess.run(['date'], capture_output=True, text=True)
    date = result.stdout.strip().split()
    day = date[2]
    abbr_month = date[1]
    if abbr_month in months:
        month = months[abbr_month]
    else:
        month = "Unknown Month"
    year = date.pop()
    return "                    "+f"{RED}System Report{RESET} - {month} {day}, {year}\n"

def device_info():
    result = subprocess.run(['hostname'], capture_output=True, text=True)
    hostname = result.stdout.strip()
    if '.' in hostname: # hostname and domain separated by a '.'
        line = hostname.split('.')
        hostname = line[0]
        domain = line[1]
    else:
        domain = "No domain"
    string_list = []
    string_list.append(f"{GREEN}Device Information{RESET}\n")
    string_list.append(f"Hostname:               {hostname}\n")
    string_list.append(f"Domain:                 {domain}\n")
    return "".join(string_list)

def network_info():
    dns_servers_result = subprocess.run(['grep', 'nameserver', '/etc/resolv.conf'], capture_output=True, text=True)
    dns_servers = [] # uses the conf file to find and store the DNS servers in the list
    gateway_result = subprocess.run(['ip', 'r'], capture_output=True, text=True) # ip route to find gateway
    ip_result = subprocess.run(['ip', 'a'], capture_output=True, text=True) # ip all to find own ip address

    ip_addr = "IP Address not found"
    net_mask_cidr = None
    for line in ip_result.stdout.splitlines():
        if 'inet ' in line:
            parts = line.strip().split()
            ip_addr = parts[1].split('/')[0] # Getting IP address before the mask in CIDR, splits the x.x.x.x/x by the / and gets index 0, x.x.x.x
            net_mask_cidr = parts[1].split('/')[1] # The network mask in CIDR, splits the x.x.x.x/x by the / and gets index 1, /x
    if net_mask_cidr:
        network_mask = str(ipaddress.IPv4Network(f"0.0.0.0/{net_mask_cidr}", strict=False).netmask) # Conversion via the ipaddress module to display the network mask
    else:
        network_mask = "Network Mask not found"

    if dns_servers_result.returncode == 0:
        for line in dns_servers_result.stdout.splitlines():
            if 'nameserver' in line:
                dns_servers.append(line.split()[1]) # the first DNS appended will be DNS 1, then DNS 2
    
    gateway = "Gateway not found"
    for line in gateway_result.stdout.splitlines():
        if 'default' in line:
            gateway = line.split()[2] # third item in this line is the gateway 'default via x.x.x.x'
    
    string_list = []
    string_list.append(f"{GREEN}Network Information{RESET}\n")
    string_list.append(f"IP Address:           {ip_addr}\n")
    string_list.append(f"Gateway:              {gateway}\n")
    string_list.append(f"Network Mask:         {network_mask}\n")
    string_list.append(f"DNS1:                 {dns_servers[0]}\n")
    string_list.append(f"DNS2:                 {dns_servers[1]}\n")
    return "".join(string_list)

def os_info():
    kernel_version_result = subprocess.run(['uname', '-r'], capture_output=True, text=True) # returns kernel version
    os_release_result = subprocess.run(['cat', '/etc/os-release'], capture_output=True, text=True) # operating system information in this file
    
    kernel_version = kernel_version_result.stdout.strip()

    for line in os_release_result.stdout.splitlines():
        if 'VERSION_ID' in line:
            version_id = line.split("=")[1].split("\"")[1] # split on the equal sign, then split on quotes. Regex could work too but I thought of this faster/first
        elif 'PRETTY_NAME' in line:
            os_name = line.split("=")[1].split("\"")[1]
        else:
            continue
    string_list = []
    string_list.append(f"{GREEN}Operating Sytem Information{RESET}\n")
    string_list.append(f"Operating System:               {os_name}\n")
    string_list.append(f"OS Version:                     {version_id}\n")
    string_list.append(f"Kernel Version:                 {kernel_version}\n")
    return "".join(string_list)

def storage_info():
    result = subprocess.run(['df', '-h'], capture_output=True, text=True) # better command to find disk usage
    for line in result.stdout.splitlines():
        if 'mapper' in line:
            sdrive_line = line.strip().split()
            total_space = round(float(sdrive_line[1].split("G")[0])) # splits to grab number before 'G'
            used_space = round(float(sdrive_line[2].split("G")[0])) # grabs the used GiB
            free_space = round(float(sdrive_line[3].split("G")[0])) # grabs the available GiB
    string_list = []
    string_list.append(f"{GREEN}Storage Information{RESET}\n")
    string_list.append(f"System Drive Total:               {total_space} GiB\n")
    string_list.append(f"System Drive Used:                {used_space} GiB\n")
    string_list.append(f"System Drive Free:                {free_space} GiB\n")
    return "".join(string_list)


def processor_info():
    result = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True) # CPU info in this file
    num_processors = 0
    for line in result.stdout.splitlines():
        if "processor" in line:
            num_processors+=1
        elif "model name" in line:
            model_name = line.strip().split(":")[1].strip() # grabs the model from the file without any spaces
        elif "cpu cores" in line:
            cores_per_processor_str = line.strip().split(":")[1].strip() # grabs the string # from the file
            cores_per_processor = int(cores_per_processor_str) # convert to int
    num_cores = num_processors * cores_per_processor
    string_list = []
    string_list.append(f"{GREEN}Processor Information{RESET}\n")
    string_list.append(f"CPU Model:                          {model_name}\n")
    string_list.append(f"Number of processors:               {num_processors}\n")
    string_list.append(f"Number of cores:                    {num_cores}\n")
    return "".join(string_list)

def memory_info():
    result = subprocess.run(['free', '-h'], capture_output=True, text=True) # better command to find RAM
    for line in result.stdout.splitlines():
        if 'Mem:' in line:
            ram_line = line.strip().split()
            total_ram = ram_line[1].split("G")[0] # accessed at line index 1, splitting to only grab number
            available_ram = ram_line[5].split("G")[0] # accessed at linx index 5, also splitting
    string_list = []
    string_list.append(f"{GREEN}Memory Information{RESET}\n")
    string_list.append(f"Total RAM:                    {total_ram} GiB\n")
    string_list.append(f"Available RAM:                {available_ram} GiB\n")
    return "".join(string_list)

def get_all_output():
    # print(create_header())
    # print(device_info())
    # print(network_info())
    # print(os_info())
    # print(storage_info())
    # print(processor_info())
    # print(memory_info())
    return

def to_log_file():
    return


def main():
    clear_screen()
    print(create_header())
    print(device_info())
    print(network_info())
    print(os_info())
    print(storage_info())
    print(processor_info())
    print(memory_info())


if __name__ == "__main__":
    main()