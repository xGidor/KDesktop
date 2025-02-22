import os
import shutil
import urllib
import zipfile
import yt_dlp as youtube_dl
from zipfile import ZipFile

FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-lgpl.zip"
FFMPEG_DIR = os.path.join(os.getcwd(), "ffmpeg")

class mp3DW:
    def __init__(self):
        self.ffmpeg_path = None
        self.downloaded = False
        self.error = ""
        self.main()

    def is_download_successful(self):
        return self.downloaded

    def is_ffmpeg_installed(self):
        """Check if ffmpeg is available in the system PATH or in the local directory."""
        # Check if ffmpeg is found in the system PATH
        if shutil.which("ffmpeg") is not None:
            return True
        
        # Check if ffmpeg is downloaded and exists in the local directory
        ffmpeg_bin_path = os.path.join(FFMPEG_DIR, "ffmpeg-master-latest-win64-lgpl", "bin", "ffmpeg.exe")
        return os.path.exists(ffmpeg_bin_path)

    def download_ffmpeg(self):
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
            'ffmpeg_location': self.ffmpeg_path,  # Use downloaded ffmpeg
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])


    def zip_mp3_files(self, directory):
        with ZipFile('playlist_mp3.zip', 'w') as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.mp3'):
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))

    def main(self):
        self.ffmpeg_path = None
        if not self.is_ffmpeg_installed():
            self.ffmpeg_path = self.download_ffmpeg()
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
            self.downloaded = False
            self.error = e
            return

        print("Video(s) downloaded successfully.")
        self.downloaded = True
        if "youtube.com/playlist?list=" in playlist_url:
            print("Zipping MP3 files...")
            self.zip_mp3_files(os.getcwd())
            print("MP3 files zipped successfully.")

        #return "Audio downloaded succesfully. Find it in KDownloads folder where KDesktop is located."

class videoDW:
    def __init__(self):
        self.ffmpeg_path = None
        self.downloaded = False
        self.error
        self.main()

    def is_download_successful(self):
        return self.downloaded

    def download_videos(self, playlist_url):
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'outtmpl': os.path.join("./KDownloads", '%(title)s.%(ext)s'),
            'quiet': True,
            'ffmpeg_location': self.ffmpeg_path,  # Use downloaded ffmpeg
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([playlist_url])
                self.downloaded = True
            except:
                self.downloaded = False

    def zip_mp3_files(self, directory):
        with ZipFile('playlist_video.zip', 'w') as zipf:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.mp3'):
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), directory))

    def main(self):
        self.ffmpeg_path = None
        if not self.is_ffmpeg_installed():
            self.ffmpeg_path = self.download_ffmpeg()
        else:
            self.ffmpeg_path = shutil.which("ffmpeg")  # Use system ffmpeg

        playlist_url = input("Enter YouTube video URL: ")
        if "soundcloud" in playlist_url:
            return
        if "&list" and "watch?v=" in playlist_url:
            playlist_url = playlist_url.split('&')[0]
        print("Downloading video... Please wait, this might take some minutes. (Any warnings can be ignored)")
        try:
            self.download_videos(playlist_url)
        except Exception as e:
            print("Error downloading videos:", e)
            self.downloaded = False
            self.error = e
            return

        print("Video(s) downloaded successfully.")
        self.downloaded = True
        if "youtube.com/playlist?list=" in playlist_url:
            print("Zipping Video files...")
            self.zip_mp3_files(os.getcwd())
            print("Video files files zipped successfully.")

        #return "Videos downloaded succesfully. Find them in KDownloads folder where KDesktop is located."
