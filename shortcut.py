#!/usr/bin/env python3

# Name
# Date

# chmod +x shortcut.py

import subprocess
import os
import time


YELLOW = '\033[38;5;220m'
GREEN = '\033[38;5;46m'
RED = '\033[38;5;196m'
BLUE = '\033[38;5;39m'
MAGENTA = '\033[38;5;213m'
RESET = '\033[0m'

def display_menu(): # Displays the main screen
    print(f"{BLUE}          **************************************{RESET}")
    print(f"{BLUE}          *********** {GREEN}Shortcut Creator{BLUE} *********{RESET}")
    print(f"{BLUE}          **************************************{RESET}")
    print(f"{GREEN}Choose an option from the menu below to begin.{RESET}")
    print(f"{MAGENTA}Menu:\n")
    print("     1 - Create a shortcut in your home directory")
    print("     2 - Remove a shortcut from your home directory")
    print(f"     3 - Run shortcut report{RESET}\n")
  

def clear_screen(): # Better readability
    os.system('clear') # clears terminal

def create_shortcut():
    return

def remove_shortcut():
    return

def shortcut_report():
    return

def main():
    menu_options = {
        '1': create_shortcut,
        '2': remove_shortcut,
        '3': shortcut_report,
        'q': lambda: False,
        'quit': lambda: False
    }
    while True:
        clear_screen() # Clearing terminal
        display_menu()

        choice = input(f'{MAGENTA}Please enter a number {GREEN}(1-3){MAGENTA} or {GREEN}"Q/q"{RESET} to quit the program: {RESET}')
        choice = choice.lower()
        if choice in menu_options:
            clear_screen()
            result = menu_options[choice]()
            if result:
                print(result + "\n")
                time.sleep(7)
            else:
                print("Quitting program: returning to terminal.")
                print(f"{YELLOW}Goodbye!{RESET}\n")
                time.sleep(4)
                clear_screen()
                break
        else:
            print()
            print(f'{RED}Invalid choice{RESET}, please select a number between {GREEN}1{RESET} through {GREEN}3{RESET} or type "Q/q" to exit.\n')
            time.sleep(5)


if __name__ == "__main__":
    main()