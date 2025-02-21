import os
import winshell
from win32com.client import Dispatch

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves up to root folder
ICON_PATH = os.path.join(ROOT_DIR, "assets", "folder_icon.ico")  # Icon file

def create_folder(folder_path):
    """Creates a folder if it doesn't exist and sets custom icon."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

        # Set custom icon
        set_folder_icon(folder_path)

def create_shortcut(target_path, shortcut_path):
    """Creates a shortcut if it doesn't exist."""
    if not os.path.exists(shortcut_path):
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.Save()
        print(f"Created shortcut: {shortcut_path}")

def set_folder_icon(folder_path):
    """Sets a custom icon for the folder."""
    desktop_ini_path = os.path.join(folder_path, "desktop.ini")

    # Write desktop.ini file to assign custom icon
    with open(desktop_ini_path, "w") as ini_file:
        ini_file.write(f"""[.ShellClassInfo]
IconResource={ICON_PATH},0
""")

    # Make desktop.ini hidden and system-protected
    os.system(f'attrib +h +s "{desktop_ini_path}"')
    os.system(f'attrib +r "{folder_path}"')  # Set folder as read-only to apply icon

def kdownloads():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    kdownloads_path = os.path.join(desktop, "KDownloads")
    shortcut_path = os.path.join(downloads, "KDownloads.lnk")

    create_folder(kdownloads_path)
    create_shortcut(kdownloads_path, shortcut_path)

def kphotos():
    pictures = os.path.join(os.path.expanduser("~"), "Pictures")
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    kphotos_path = os.path.join(pictures, "KPhotos")
    shortcut_path = os.path.join(downloads, "KPhotos.lnk")

    create_folder(kphotos_path)
    create_shortcut(kphotos_path, shortcut_path)

def kvideos():
    videos = os.path.join(os.path.expanduser("~"), "Videos")
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    kvideos_path = os.path.join(videos, "KVideos")
    shortcut_path = os.path.join(downloads, "KVideos.lnk")

    create_folder(kvideos_path)
    create_shortcut(kvideos_path, shortcut_path)

def kdocuments():
    documents = os.path.join(os.path.expanduser("~"), "Documents")
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    kdocuments_path = os.path.join(documents, "KDocuments")
    shortcut_path = os.path.join(downloads, "KDocuments.lnk")

    create_folder(kdocuments_path)
    create_shortcut(kdocuments_path, shortcut_path)

def kzips():
    documents = os.path.join(os.path.expanduser("~"), "Documents")
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    kzips_path = os.path.join(documents, "KZip")
    shortcut_path = os.path.join(downloads, "KZip.lnk")

    create_folder(kzips_path)
    create_shortcut(kzips_path, shortcut_path)

def kmusic():
    music = os.path.join(os.path.expanduser("~"), "Music")
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    kmusic_path = os.path.join(music, "KMusic")
    shortcut_path = os.path.join(downloads, "KMusic.lnk")

    create_folder(kmusic_path)
    create_shortcut(kmusic_path, shortcut_path)

def check_folders():
    kdownloads()
    kphotos()
    kvideos()
    kdocuments()
    kzips()
    kmusic()
