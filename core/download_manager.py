import os
import shutil
import time

# Define where files should be moved based on their extensions
FILE_SORTING_RULES = {
    "KDownloads": [".exe", ".msi", ".iso"],
    "KPhotos": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "KVideos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg"],
    "KDocuments": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "KZip": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "KMusic": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"]
}

# Exclude KFolder shortcuts from being moved
EXCLUDED_FILES = [f"KDownloads.lnk", f"KPhotos.lnk", f"KVideos.lnk", f"KDocuments.lnk", f"KZip.lnk", f"KMusic.lnk"]


# Get user directories
USER_HOME = os.path.expanduser("~")
DOWNLOADS_DIR = os.path.join(USER_HOME, "Downloads")
DESKTOP_DIR = os.path.join(USER_HOME, "Desktop")
PICTURES_DIR = os.path.join(USER_HOME, "Pictures")
VIDEOS_DIR = os.path.join(USER_HOME, "Videos")
DOCUMENTS_DIR = os.path.join(USER_HOME, "Documents")
MUSIC_DIR = os.path.join(USER_HOME, "Music")

# Define target folders
TARGET_FOLDERS = {
    "KDownloads": os.path.join(DESKTOP_DIR, "KDownloads"),
    "KPhotos": os.path.join(PICTURES_DIR, "KPhotos"),
    "KVideos": os.path.join(VIDEOS_DIR, "KVideos"),
    "KDocuments": os.path.join(DOCUMENTS_DIR, "KDocuments"),
    "KZip": os.path.join(DOCUMENTS_DIR, "KZip"),
    "KMusic": os.path.join(MUSIC_DIR, "KMusic"),
}

def get_target_folder(file_extension):
    """Return the correct folder for a given file extension."""
    for folder, extensions in FILE_SORTING_RULES.items():
        if file_extension.lower() in extensions:
            return TARGET_FOLDERS[folder]
    return TARGET_FOLDERS["KDownloads"]  # Default to KDownloads

def move_files():
    """Move files from Downloads to the appropriate folders."""
    filefound = False

    for file in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, file)

        # Skip directories and excluded files (shortcuts)
        if os.path.isdir(file_path) or file in EXCLUDED_FILES or ".crdownload" in file:
            continue

        # Get file extension
        file_extension = os.path.splitext(file)[1]

        # Find target folder
        target_folder = get_target_folder(file_extension)
        target_path = os.path.join(target_folder, file)
        filefound = True
        # Move file
        shutil.move(file_path, target_path)

    return filefound