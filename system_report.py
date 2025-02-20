#!/usr/bin/env python3

# Name
# Date

# chmod +x system_report.py

import subprocess
import os
import re
import platform
import ipaddress


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
    return "                       "+f"{RED}System Report{RESET} - {month} {day}, {year}\n\n"

def device_info():
    result = subprocess.run(['hostname'], capture_output=True, text=True)
    hostname = result.stdout.strip()
    if '.' in hostname: # hostname and domain separated by a '.'
        line = hostname.split('.', 1)
        hostname = line[0]
        domain = line[1] if len(line) > 1 else "No domain" # edit: can't split hostname and domain by 1 period -> myhost.mydomain.com
    else:
        domain = "No domain"
    if domain == "localdomain":
        domain = "localdomain (default domain)" # default domain is technically not a domain?
    string_list = []
    string_list.append(f"{GREEN}Device Information{RESET}\n")
    string_list.append(f"Hostname:                       {hostname}\n")
    string_list.append(f"Domain:                         {domain}\n\n")
    return "".join(string_list)

def network_info():
    dns_servers_result = subprocess.run(['grep', 'nameserver', '/etc/resolv.conf'], capture_output=True, text=True)
    dns_servers = ["DNS not found", "DNS not found"] # uses the conf file to find and store the DNS servers in the list
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
                dns_servers.insert(0, line.split()[1]) # the first DNS inserted will be DNS 1, then DNS 2
                dns_servers.pop()
    
    gateway = "Gateway not found"
    for line in gateway_result.stdout.splitlines():
        if 'default' in line:
            gateway = line.split()[2] # third item in this line is the gateway 'default via x.x.x.x'
    
    string_list = []
    string_list.append(f"{GREEN}Network Information{RESET}\n")
    string_list.append(f"IP Address:                     {ip_addr}\n")
    string_list.append(f"Gateway:                        {gateway}\n")
    string_list.append(f"Network Mask:                   {network_mask}\n")
    string_list.append(f"DNS1:                           {dns_servers[0]}\n")
    string_list.append(f"DNS2:                           {dns_servers[1]}\n\n")
    return "".join(string_list)

def os_info():
    os_name = "Operating System Name not found"
    version_id = "OS version not found"
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
    string_list.append(f"Kernel Version:                 {kernel_version}\n\n")
    return "".join(string_list)

def storage_info():
    total_space = "Unknown"
    used_space = "Unknown"
    free_space = "Unknown"
    total_unit = "Error: Unit not found"
    used_unit = "Error: Unit not found"
    free_unit = "Error: Unit not found"
    unit_options = {
        'G': "GB",
        'K': "KB",
        'M': "MB",
        'T': "TB",
        'P': "PB"

    } # different units are used
    result = subprocess.run(['df', '-h'], capture_output=True, text=True) # better command to find disk usage
    for line in result.stdout.splitlines():
        if 'mapper' in line:
            sdrive_line = line.strip().split()
            for key in unit_options:
                if key in sdrive_line[1]:
                    total_space = round(float(sdrive_line[1].split(key)[0])) # splits to grab number before the unit
                    total_unit = unit_options[key]
                if key in sdrive_line[2]:
                    used_space = round(float(sdrive_line[2].split(key)[0])) # grabs the used space in the line
                    used_unit = unit_options[key]
                if key in sdrive_line[3]:
                    free_space = round(float(sdrive_line[3].split(key)[0])) # grabs the available in the line
                    free_unit = unit_options[key]
    string_list = []
    string_list.append(f"{GREEN}Storage Information{RESET}\n")
    string_list.append(f"System Drive Total:             {total_space} {total_unit}\n")
    string_list.append(f"System Drive Used:              {used_space} {used_unit}\n")
    string_list.append(f"System Drive Free:              {free_space} {free_unit}\n\n")
    return "".join(string_list)


def processor_info():
    result = subprocess.run(['cat', '/proc/cpuinfo'], capture_output=True, text=True) # CPU info in this file
    num_processors = 0
    for line in result.stdout.splitlines():
        if "processor" in line:
            num_processors+=1 # each processor has an entry
        elif "model name" in line:
            model_name = line.strip().split(":")[1].strip() # grabs the model from the file without any spaces
        elif "cpu cores" in line:
            cores_per_processor_str = line.strip().split(":")[1].strip() # grabs the string # from the file
            cores_per_processor = int(cores_per_processor_str) # convert to int
    num_cores = num_processors * cores_per_processor # total cores is the processors * core per processor
    string_list = []
    string_list.append(f"{GREEN}Processor Information{RESET}\n")
    string_list.append(f"CPU Model:                      {model_name}\n")
    string_list.append(f"Number of processors:           {num_processors}\n")
    string_list.append(f"Number of cores:                {num_cores}\n\n")
    return "".join(string_list)

def memory_info():
    total_ram = "Total RAM not found"
    available_ram = "Available RAM not found"
    total_ram_unit = "Error: Unit not found"
    available_ram_unit = "Error: Unit not found"
    unit_options = {
        'G': "GiB",
        'M': "MiB",
        'B': "B",
        'T': "TiB",
        'P': "PiB"
    } # different units are used
    result = subprocess.run(['free', '-h'], capture_output=True, text=True) # better command to find RAM
    for line in result.stdout.splitlines():
        if 'Mem:' in line:
            ram_line = line.strip().split()
            for key in unit_options:
                if key in ram_line[1]:
                    total_ram = ram_line[1].split(key)[0] # accessed at line index 1, splitting to only grab number
                    total_ram_unit = unit_options[key]
                if key in ram_line[6]:
                    available_ram = ram_line[6].split(key)[0] # accessed at linx index 6, also splitting
                    available_ram_unit = unit_options[key]
    string_list = []
    string_list.append(f"{GREEN}Memory Information{RESET}\n")
    string_list.append(f"Total RAM:                      {total_ram} {total_ram_unit}\n")
    string_list.append(f"Available RAM:                  {available_ram} {available_ram_unit}\n\n")
    return "".join(string_list)

def get_all_output(): # getting all output as a string
    string_list = []
    string_list.append(create_header())
    string_list.append(device_info())
    string_list.append(network_info())
    string_list.append(os_info())
    string_list.append(storage_info())
    string_list.append(processor_info())
    string_list.append(memory_info())
    return "".join(string_list)

def remove_ansi_colors(text):
    ansi_escape = re.compile(r'\033\[[0-9;]*m') # regular expression for ANSI color codes which need to be removed
    return ansi_escape.sub('', text)

def to_log_file(text):
    clean_text = remove_ansi_colors(text) # removes color codes so log file isn't silly looking
    hostname = platform.node() # another way to get the hostname
    home_dir = os.path.expanduser("~") # expanding to user home directory
    log_file_path = os.path.join(home_dir, f"{hostname}_system_report.log") # log file path
    with open(log_file_path, 'w') as file: 
        file.write(clean_text)


def main():
    clear_screen()
    all_output = get_all_output()
    print(all_output, end="")
    to_log_file(all_output)

if __name__ == "__main__":
    main()