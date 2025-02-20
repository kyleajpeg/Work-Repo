#!/usr/bin/env python3

# Name
# Date

# chmod +x ping_test.py

import subprocess
import os
import time

RIT_DNS = '129.21.3.17'
GOOGLE = 'www.google.com'

YELLOW = '\033[38;5;220m'
GREEN = '\033[38;5;46m'
RED = '\033[38;5;196m'
BLUE = '\033[38;5;39m'
MAGENTA = '\033[38;5;213m'
RESET = '\033[0m'

def display_menu(): # Displays the main screen
    print(f"{BLUE}**************************************{RESET}")
    print(f"{BLUE}*********** {GREEN}Ping Test Tool{BLUE} ***********{RESET}")
    print(f"{BLUE}**************************************{RESET}")
    print(f"{GREEN}Choose an option from the menu below to begin.{RESET}")
    print(f"{MAGENTA}Menu:\n")
    print("     1 - Display the default gateway")
    print("     2 - Test Local Connectivity")
    print("     3 - Test Remote Connectivity")
    print("     4 - Test DNS Resolution")
    print(f"     5 - Exit{RESET}\n")

def clear_screen(): # Probably don't need this to be a fxn
    os.system('clear') # clears terminal

def get_gateway(flag=False):
    # Using 'ip r' to find gateway on linux
    result = subprocess.run(['ip', 'r'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if 'default' in line:
            gateway = line.split()[2] # "default via x.x.x.x" 0 1 2
            if flag:
                return gateway
            else:
                print("Default gateway:")
                return f"{GREEN}{gateway}{RESET}" 
    return f"{RED}Gateway not found{RESET}"

def local_connectivity_test(): # Pinging the gateway to test local connectivity
    gateway = get_gateway(True)
    print(f"{YELLOW}Testing local connectivity to your gateway ({MAGENTA}{gateway}{YELLOW})...{RESET}")
    result = subprocess.run(['ping', '-c', '4', gateway], capture_output=True, text=True)
    if result.returncode == 0:
        return f"Local connectivity test {GREEN}passed.{RESET}"
    else:
        return f"Local connectivity test {RED}failed.{RESET}"

def remote_connectivity_test(): # Pinging remote IP for remote test (RIT's DNS)
    print(f"{YELLOW}Testing remote connectivity, trying IP address {MAGENTA}{RIT_DNS}{YELLOW} ...{RESET}")
    result = subprocess.run(['ping', '-c', '4', RIT_DNS], capture_output=True, text=True)
    if result.returncode == 0:
        return f"Remote connectivity test {GREEN}passed.{RESET}"
    else:
        return f"Remote connectivity test {RED}failed.{RESET}"

def dns_resolution_test(): # Using 'nslookup' & google for DNS resolution test
    print(f"{YELLOW}Resolving DNS: Trying URL {MAGENTA}{GOOGLE}{YELLOW} ...{RESET}")
    result = subprocess.run(['nslookup', GOOGLE], capture_output=True, text=True)
    if 'authoritative' in result.stdout.lower(): # Checking if authoritative is in the output (successful lookup)
        return f"DNS resolution test {GREEN}passed.{RESET}"
    else:
        return f"DNS resolution test {RED}failed.{RESET}"

def main():
    menu_options = {
        '1': get_gateway,
        '2': local_connectivity_test,
        '3': remote_connectivity_test,
        '4': dns_resolution_test,
        '5': lambda: False
    }
    while True:
        clear_screen() # Clearing terminal
        display_menu()

        choice = input(f"{MAGENTA}Enter your choice {GREEN}(1-5){MAGENTA} to run the given command: {RESET}")
        if choice in menu_options:
            clear_screen()
            result = menu_options[choice]()
            if result:
                print(result + "\n")
                time.sleep(7)
            else:
                print("Exiting...\n")
                break
        else:
            clear_screen()
            print(f"{RED}Invalid choice{RESET}, please select between {GREEN}1{RESET} and {GREEN}5{RESET}.\n")
            time.sleep(5)


if __name__ == "__main__":
    main()
