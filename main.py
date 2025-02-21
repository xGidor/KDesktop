# KDesktop-Manager (Kazi-Desktop) created by Gidor

import ctypes
import os
import subprocess
import time
import sys
import schedule

VERSION = "1.0"

from core import folder_structure, download_manager

def task():
    """The function that runs every minute."""
    folder_structure.check_folders()

    did_cleanup = download_manager.move_files()

    if did_cleanup:
        print("Desktop cleanup done.")

def set_process_name():
    """Set the process Windows Title if ran in Console mode""" # regardless of which mode it is running in, task manager will show Python.exe
    ctypes.windll.kernel32.SetConsoleTitleW("KDesktop")

if __name__ == "__main__":
    set_process_name()
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

    task()  # Execute task right at start then rest executions will come from the loop

    # Run the task every few seconds
    schedule.every(3).seconds.do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)