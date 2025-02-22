import os
import shutil
import urllib
import zipfile
import yt_dlp as youtube_dl
from zipfile import ZipFile
from yt_dlp.postprocessor import FFmpegPostProcessor

FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-lgpl.zip"
FFMPEG_DIR = os.path.join(os.getcwd(), "ffmpeg")

def is_ffmpeg_installed():
    """Check if ffmpeg is available in the system PATH or in the local directory."""
    # Check if ffmpeg is found in the system PATH
    if shutil.which("ffmpeg") is not None:
        return True
    
    # Check if ffmpeg is downloaded and exists in the local directory
    ffmpeg_bin_path = os.path.join(FFMPEG_DIR, "ffmpeg-master-latest-win64-lgpl", "bin", "ffmpeg.exe")
    FFmpegPostProcessor._ffmpeg_location.set(ffmpeg_bin_path)
    return os.path.exists(ffmpeg_bin_path)

def download_ffmpeg():
    """Download and extract ffmpeg if not installed."""
    if not os.path.exists(FFMPEG_DIR):
        os.makedirs(FFMPEG_DIR)
    zip_path = os.path.join(FFMPEG_DIR, "ffmpeg.zip")
    print("Downloading ffmpeg... This may take a moment.")
    urllib.request.urlretrieve(FFMPEG_URL, zip_path)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(FFMPEG_DIR)
    os.remove(zip_path)
    
    # Find extracted folder and set the correct binary path
    extracted_folder = [f for f in os.listdir(FFMPEG_DIR) if os.path.isdir(os.path.join(FFMPEG_DIR, f))][0]
    ffmpeg_bin_path = os.path.join(FFMPEG_DIR, extracted_folder, "bin")
    print(f"ffmpeg installed at: {ffmpeg_bin_path}")
    return ffmpeg_bin_path

class mp3DW:
    def __init__(self):
        self.ffmpeg_path = None
        self.main()

    def download_videos(self, playlist_url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join("./KDownloads", '%(title)s.%(ext)s'),
            'quiet': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([playlist_url])
            except Exception as e:
                print("Couldn't download video: ", e)

    def zip_mp3_files(self, directory):
        with ZipFile('playlist_mp3.zip', 'w') as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.mp3'):
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))

    def main(self):
        if not is_ffmpeg_installed():
            self.ffmpeg_path = download_ffmpeg()
        else:
            self.ffmpeg_path = shutil.which("ffmpeg")  # Use system ffmpeg

        playlist_url = input("Enter YouTube/SoundCloud URL: ")
        if "&list" and "watch?v=" in playlist_url:
            playlist_url = playlist_url.split('&')[0]
        print("Downloading audio... Please wait, this might take some minutes. (Any warnings can be ignored)")
        try:
            self.download_videos(playlist_url)
        except Exception as e:
            print("Error downloading videos:", e)
            return

        print("Video(s) downloaded successfully.")
        if "youtube.com/playlist?list=" in playlist_url:
            print("Zipping Audio files...")
            self.zip_mp3_files(os.getcwd())
            print("Audio files zipped successfully.")

class videoDW:
    def __init__(self):
        self.ffmpeg_path = None
        self.main()

    def download_videos(self, playlist_url):
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'outtmpl': os.path.join("./KDownloads", '%(title)s.%(ext)s'),
            'quiet': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([playlist_url])
            except Exception as e:
                print("Couldn't download video: ", e)

    def zip_mp3_files(self, directory):
        with ZipFile('playlist_video.zip', 'w') as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.mp3'):
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))


    def main(self):
        if not self.is_ffmpeg_installed():
            self.ffmpeg_path = self.download_ffmpeg()
        else:
            self.ffmpeg_path = shutil.which("ffmpeg")  # Use system ffmpeg

        playlist_url = input("Enter YouTube video URL: ")
        if "soundcloud" in playlist_url:
            return
        if "&list" and "watch?v=" in playlist_url:
            playlist_url = playlist_url.split('&')[0]
        print("Downloading videos... Please wait, this might take some minutes. (Any warnings can be ignored)")
        try:
            self.download_videos(playlist_url)
        except Exception as e:
            print("Error downloading videos:", e)
            return

        print("Video(s) downloaded successfully.")
        if "youtube.com/playlist?list=" in playlist_url:
            print("Zipping MP3 files...")
            self.zip_mp3_files(os.getcwd())
            print("Video(s) files zipped successfully.")

