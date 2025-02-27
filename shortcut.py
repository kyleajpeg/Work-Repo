#!/usr/bin/env python3

# Name
# Date

# chmod +x shortcut.py

from pathlib import Path
import os
import time
import sys
import subprocess


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

def user_continue(): # sick of retyping this also maybe better readability idk
    input("\nPress Enter to continue...")

def find_files_by_name(filename):
    """Find all files with the given name on the system"""
    try:
        # using the find command to search for regular files, also lets ignore any errors to /dev/null
        result = subprocess.run(['find', '/', '-name', filename, '-type', 'f', '2>/dev/null'], capture_output=True, text=True, shell=True)
        files = result.stdout.strip().split('\n')
        files = [file for file in files if file] # quick list comp to remove the empty strings
        return files
    except subprocess.SubprocessError as e: # can't find the file(s)
        print(f"\n{RED}Error searching for files: {RESET}\n{e}")
        return []


def create_shortcut():
    """Creates a symbolic link to a file on the user's desktop"""
    print(f"{GREEN}===== Create a Shortcut ====={RESET}\n")
    
    # getting the filename to search for
    filename = input(f"Enter the {MAGENTA}name{RESET} of the file you want to create a shortcut for: ")
    
    if not filename: # if empty string
        print(f"\n{RED}Error: You must enter a filename.{RESET}")
        user_continue()
        return True
    
    # finding all files on the system with that name
    print(f"\n{BLUE}Searching for files named '{filename}'...{RESET}")
    files = find_files_by_name(filename)
    
    if not files: # handling if the file(s) wasn't found
        print(f"\n{RED}Error: No files named '{filename}' were found on the system.{RESET}")
        user_continue()
        return True
    
    target_path = ""
    
    # user will select which file if there are multiple
    if len(files) > 1:
        print(f"\n{YELLOW}Multiple files with the name '{filename}' were found:{RESET}")
        for i, file in enumerate(files, 1): # prints options cleanly
            print(f"[{i}] {file}")
        
        while True:
            try:
                choice = input(f"\nPlease select the file you want to create a shortcut for {GREEN}(1-{len(files)}){RESET}: ")
                print(f"Or, enter {GREEN}'Q/q'{RESET} to quit & return to the main menu")
                if choice.lower() == 'q':
                    print("Returning to main menu...")
                    time.sleep(3)
                    return True
                choice_i = int(choice) - 1
                if 0 <= choice_i < len(files):
                    target_path = files[choice_i]
                    break
                else:
                    print(f"\n{RED}Invalid selection. Please enter a number between {GREEN}1{RED} and {GREEN}{len(files)}{RED}.{RESET}")
                    time.sleep(5.5)
                    sys.stdout.write("\033[5A")
                    sys.stdout.write("\033[J")
                    sys.stdout.flush()
            except ValueError:
                print(f"\n{RED}Invalid input. Please enter a number {GREEN}(1-{len(files)}){RESET}")
                time.sleep(5.5)
                sys.stdout.write("\033[5A")
                sys.stdout.write("\033[J")
                sys.stdout.flush()
    else:
        # if only one file is found, assume its the one the user is talking about and use it automatically
        target_path = files[0]
        print(f"\n{GREEN}Found file: {target_path}{RESET}")
    
    # get the desktop path
    desktop_path = Path.home() / 'Desktop'
    
    # basename used to grab the last part of the filepath, the filename
    shortcut_basename = os.path.basename(target_path)
    
    # appending the name to the desktop path to create the full shortcut path
    shortcut_path = os.path.join(desktop_path, shortcut_basename)
    
    # check if a file (shortcut) exists at that path. Checking if a file has this name already.
    result = subprocess.run(['test', '-e', shortcut_path])
    if result.returncode == 0:
        overwrite = input(f"\n{YELLOW}A file/shortcut with that name already exists. Overwrite? (y/n): {RESET}").lower()
        if overwrite != 'y':
            print("\nShortcut creation cancelled.")
            user_continue()
            return True
        try:
            subprocess.run(['rm', shortcut_path], check=True)
        except subprocess.SubprocessError as e:
            print(f"\n{RED}Error removing existing file: {RESET}\n{e}")
            user_continue()
            return True
    
    # using os module to create a symbolic link and error handling
    try:
        os.symlink(shortcut_path, shortcut_basename)
        print(f"{GREEN}Shortcut created successfully at {shortcut_path}{RESET}")
    except PermissionError:
        print(f"{RED}Permission denied: You don't have permission to create a shortcut at {shortcut_path}{RESET}")
    except Exception as e:
        print(f"{RED}Error creating shortcut: {RESET}\n{e}")
    user_continue()
    return True


def find_links_by_path(path): # only checking the surface level of desktop with maxdepth at 1
    result = subprocess.run(['find', path, '-type', 'l', '-maxdepth', '1'], capture_output=True, text=True, check=True)
    symlinks = result.stdout.strip().split('\n')
    # removing empty strings again
    symlinks = [link for link in symlinks if link]
    return symlinks

def display_links(links_list):
    for i, link in enumerate(links_list, 1):
        # get the target path of the symbolic link using os readlink
        target = os.readlink(link)
        
        # get the filename using basename
        link_name = os.path.basename(link)
        
        print(f"{i}. {link_name} -> {target}")

def remove_shortcut():
    print(f"{GREEN}===== Remove a Shortcut ====={RESET}\n")
    
    # get the desktop path
    desktop_path = Path.home() / 'Desktop'
    
    # finding all symbolic links on desktop and putting in a list
    try: 
        desktop_symlinks = find_links_by_path(desktop_path)
    except subprocess.SubprocessError as e:
        print(f"\n{RED}Error finding shortcuts: {RESET}\n{e}")
        user_continue()
        return True
    
    if not desktop_symlinks: # empty list, no shortcuts, nothing to do
        print(f"{YELLOW}No shortcuts found on the Desktop.{RESET}")
        user_continue()
        return True
    
    # display the symbolic links already on the desktop
    print(f"{BLUE}Shortcuts on the Desktop:{RESET}\n")
    display_links(desktop_symlinks)
    
    # asking user which link to remove 
    while True:
        try:
            choice = input(f"\nEnter the {MAGENTA}number{RESET} of the shortcut to remove (or {RED}'C/c'{RESET} to cancel): ")
            
            if choice.lower() == 'c':
                print("\nOperation cancelled.")
                break # back to menu
            
            choice_i = int(choice) - 1
            if 0 <= choice_i < len(desktop_symlinks):
                link_to_remove = desktop_symlinks[choice_i]
                
                # grab basename to confirm link to remove
                link_name = os.path.basename(link_to_remove)
                
                confirm = input(f"\n{YELLOW}Are you sure you want to remove {MAGENTA}'{link_name}'{YELLOW}? (y/n): {RESET}").lower()
                if confirm == 'y':
                    try:
                        subprocess.run(['rm', link_to_remove], check=True)
                        print(f"\n{GREEN}Shortcut '{link_name}' removed successfully.{RESET}")
                    except subprocess.SubprocessError as e:
                        print(f"\n{RED}Error removing shortcut: {RESET}\n{e}")
                else:
                    print("\nRemoval cancelled.")
                break # back to menu
            else:
                print(f"\n{RED}Invalid selection.{RESET} Please enter a number between {GREEN}1{RESET} and {GREEN}{len(desktop_symlinks)}{RESET}.")
        except ValueError:
            print(f"\n{RED}Invalid input. Please enter a number or {RED}'C/c'{RESET} to cancel.")
    
    user_continue()
    return True

def shortcut_report():
    print(f"{GREEN}===== Shortcut Report ====={RESET}\n")
    
    # displaying the current directory (which should always be the home directory)
    result = subprocess.run(['pwd'], capture_output=True, text=True)
    print(f"Current working directory: {result.stdout.strip()}\n")
    
    # get the desktop path
    desktop_path = Path.home() / 'Desktop'

    try: 
        desktop_symlinks = find_links_by_path(desktop_path)
    except subprocess.SubprocessError as e:
        print(f"\n{RED}Error finding shortcuts: {RESET}\n{e}")
        user_continue()
        return True
    
    # print number of symbolic links/shortcuts
    print(f"The number of links is {BLUE}{len(desktop_symlinks)}{RESET}\n")
    
    # display the symbolic links
    print(f"{BLUE}Shortcut{RESET} -> {YELLOW}Target Path{RESET}")
    if desktop_symlinks:
        display_links(desktop_symlinks)
    
    user_continue()
    return True

def main():
    os.chdir(Path.home()) # stay in home dir
    menu_options = {
        '1': create_shortcut,
        '2': remove_shortcut,
        '3': shortcut_report,
        'q': lambda: False,
        'quit': lambda: False,
        'exit': lambda: False
    }
    while True:
        clear_screen() # Clearing terminal
        display_menu()

        choice = input(f'{MAGENTA}Please enter a number {GREEN}(1-3){MAGENTA} or {GREEN}"Q/q"{MAGENTA} to quit the program: {RESET}')
        choice = choice.lower()
        if choice in menu_options:
            clear_screen()
            result = menu_options[choice]()
            if result:
                result
            else:
                print()
                print("Quitting program: returning to terminal.")
                print()
                print(f"{YELLOW}Goodbye!{RESET}\n")
                time.sleep(4)
                clear_screen()
                break
        else:
            print()
            print(f'{RED}Invalid choice{RESET}, please select a number between {GREEN}1{RESET} and {GREEN}3{RESET}\nor type {GREEN}"Q/q"{RESET} to exit.\n')
            time.sleep(5)


if __name__ == "__main__":
    main()