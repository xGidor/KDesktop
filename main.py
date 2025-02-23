# KDesktop (KaziDesktop) created by Gidor

import ctypes
import json
import os
import subprocess
import time
import threading
import sys
import pyperclip
import schedule

VERSION = "1.0"

from core.downloader import mp3DW as MP3Downloader
from core.downloader import videoDW as VideoDownloader
from core import folder_structure, download_manager

CONFIG_FILE = "config.json"

# Default settings
config = {
    "is_sorting_enabled": False,
    "is_clipboard_enabled": False,
    "max_saved_clipboard": 25,
    "saved_clipboard": [],
    "is_autostart_enabled": False,
    "autostart_paths": []
}

in_menu_console = False

def clear_term():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config():
    """Loads the configuration from config.json if it exists."""
    global config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in config file. Using defaults.")
    else:
        print("No config file found. Using defaults.")
        save_config()  # Save defaults if config file doesn't exist

def save_config():
    """Saves the current configuration to config.json."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        print("Configuration saved successfully.")
    except Exception as e:
        print(f"Error saving config: {e}")

def set_process_name():
    """Set the process Windows Title if ran in Console mode""" # regardless of which mode it is running in, task manager will show Python.exe
    ctypes.windll.kernel32.SetConsoleTitleW("KDesktop")

def task():
    """The function that runs every minute."""
    folder_structure.check_folders()

    did_cleanup = download_manager.move_files()

    if did_cleanup:
        if in_menu_console:
            clear_term()
            print_defaults()
            print("[Download Sorting] Task executed.\n")
            print("[1] Download Sorting\n[2] Clipboard Manager\n[3] Autostart programs\n[4] Media Downloader\n[q] Exit KDekstop\n\nType your choice: ")

def task_scheduler():
    """Runs the scheduled task in a separate thread."""
    
    # Run the task immediately at startup
    task()

    # Schedule the task every 3 seconds (adjust as needed)
    schedule.every(3).seconds.do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)

def clipboard_monitor():
    """Monitors the clipboard and saves unique copied text."""
    while True:
        if config["is_clipboard_enabled"]:
            clipboard_content = pyperclip.paste()

            if clipboard_content and clipboard_content not in config["saved_clipboard"]:
                # Add new text to the clipboard history
                config["saved_clipboard"].append(clipboard_content)
                
                # Keep only the last `max_saved_clipboard` items
                if len(config["saved_clipboard"]) > config["max_saved_clipboard"]:
                    config["saved_clipboard"].pop(0)

                save_config()
                if in_menu_console:
                    clear_term()
                    print_defaults()
                    print(f"[Clipboard Manager] New entry added: {clipboard_content}\n")
                    print("[1] Download Sorting\n[2] Clipboard Manager\n[3] Autostart programs\n[4] Media Downloader\n[q] Exit KDekstop\n\nType your choice: ")

        time.sleep(1)  # Prevent high CPU usage

def console_menu():
    global in_menu_console
    while True:
        print_defaults()
        in_menu_console = True
        choice = input("[1] Download Sorting\n[2] Clipboard Manager\n[3] Autostart programs\n[4] Media Downloader\n[q] Exit KDekstop\n\nType your choice: ")
        match choice:
            case  "q":
                clear_term()
                print("Exiting KDesktop...")
                sys.exit()
                break
            case "1":
                while True:
                    clear_term()
                    in_menu_console = False
                    switch = input("Download Sorting is a feature that automaticaly sorts your downloaded files into the corresponding folders, example: Photos in the Photos folder.\nKDesktop automatically creates shortcuts for these folders in your Download folder.\n\n[1] Turn download sorting ON\n[2] Turn download sorting OFF\n[c] Cancel\n\nWhat do you want to do?: ")
                    if switch.lower() not in ["1", "2", "c"]:
                        clear_term()
                        continue
                    if switch.lower() == "c":
                        clear_term()
                        break
                    if switch == "1":
                        if not config["is_sorting_enabled"]:
                            clear_term()
                            config["is_sorting_enabled"] = True
                            sorting_thread = threading.Thread(target=task_scheduler, daemon=True)
                            sorting_thread.start()
                            print("Download sorting has been enabled.")
                            save_config()
                            break
                        clear_term()
                        print("Download sorting is already enabled.")
                        break
                    if switch == "2":
                        if config["is_sorting_enabled"]:
                            clear_term()
                            config["is_sorting_enabled"] = False
                            print("Download sorting has been disabled.")
                            save_config()
                            break
                        clear_term()
                        print("Download sorting is already disabled.")
                        break
            case "2":
                while True:
                    clear_term()
                    in_menu_console = False
                    switch = input("Clipboard Manager saves your copied texts into KDesktop and you can view them whenever you want.\n[1] Enable Clipboard Manager\n[2] Disable Clipboard Manager\n[3] Set maximum saved count\n[4] View clipboard\n[5] Clear clipboard\n[c] Cancel\n\nWhat do you want to do?: ")

                    if switch.lower() not in ["1", "2", "3", "4", "5", "c"]:
                        continue
                    if switch.lower() == "c":
                        break
                    if switch == "1":
                        if not config["is_clipboard_enabled"]:
                            config["is_clipboard_enabled"] = True
                            clipboard_thread = threading.Thread(target=clipboard_monitor, daemon=True)
                            clipboard_thread.start()
                            save_config()
                            print("Clipboard Manager has been enabled.")
                        else:
                            print("Clipboard Manager is already enabled.")
                        break
                    if switch == "2":
                        if config["is_clipboard_enabled"]:
                            config["is_clipboard_enabled"] = False
                            save_config()
                            print("Clipboard Manager has been disabled.")
                        else:
                            print("Clipboard Manager is already disabled.")
                        break
                    if switch == "3":
                        while True:
                            in_menu_console = False
                            clear_term()
                            try:
                                count = int(input("Type in how many clipboard messages do you want to save maximum: "))
                                if 10 <= count <= 100:
                                    clear_term()
                                    print(f"Clipboard Manager maximum set to {count}.")
                                    break 
                                else:
                                    clear_term()
                                    print("Incorrect number set! The maximum number you can set is 100, and the minimum is 10. Default: 25")
                                    break
                            except ValueError:
                                clear_term()
                                print("Incorrect number set! Please type in a number.")
                                break
                        break   
                    if switch == "4":
                        clear_term()
                        
                        if config["saved_clipboard"]:  # Check if the list is not empty
                            print("Saved clipboard contents:\n")
                            for index, item in enumerate(config["saved_clipboard"], start=1):
                                print(f"{index}. {item}")
                        else:
                            print("Clipboard is empty.")
                        
                        input("\nPress Enter to continue...")  # Pause before returning to the loop   
                        clear_term()
                        break                     
                    if switch == "5":
                        clear_term()
                        choice = input("Are you sure you want to clear your clipboard? (y/n, default: yes): ")
                        if choice in ["no", "n"]:
                            clear_term()
                            break

                        config["saved_clipboard"] = []
                        pyperclip.copy("") # Also clears the windows clipboard

                        clear_term()
                        print("Clipboard was cleared successfully.")
                        break
            case "3":
                clear_term()
                pass 
            case "4":
                while True:
                    clear_term()
                    in_menu_console = False
                    switch = input("""[1] MP3 Downloader (Audio)\n[2] MP4 Downloader (Video)\n[c] Cancel\nWhat do you want to do?: """)
                    if switch.lower() not in ["1", "2", "c"]:
                        clear_term()
                        continue
                    if switch.lower() == "c":
                        clear_term()
                        break
                    if switch == "1":
                        clear_term()
                        MP3Downloader()

                        break
                    if switch == "2":
                        clear_term()
                        VideoDownloader()  
                        break
            case _:
                clear_term()
                continue


def print_defaults():
    print(""" _   _______          _    _              
| | / /  _  \\        | |  | |             
| |/ /| | | |___  ___| | _| |_ ___  _ __  
|    \\| | | / _ \\/ __| |/ / __/ _ \\| '_ \\ 
| |\\  \\ |/ /  __/\\__ \\   <| || (_) | |_) |
\\_| \\_/___/ \\___||___/_|\\_\\\\__\\___/| .__/ 
                                   | |    
                                   |_|    """)
    print("Created by: Gidor")
    print("Version: " + VERSION + "\n")


if __name__ == "__main__":
    load_config()  # Load the configuration at startup
    set_process_name()

    # Start the task scheduler in a separate thread if sorting is enabled
    if config["is_sorting_enabled"]:
        sorting_thread = threading.Thread(target=task_scheduler, daemon=True)
        sorting_thread.start()

    # Start clipboard monitoring if enabled
    if config["is_clipboard_enabled"]:
        clipboard_thread = threading.Thread(target=clipboard_monitor, daemon=True)
        clipboard_thread.start()

    # Run the console menu in the main thread
    console_menu()