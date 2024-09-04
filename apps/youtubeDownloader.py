import threading
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from pytube import YouTube
from pytube.exceptions import RegexMatchError
from pytube.innertube import _default_clients
from pytube import cipher
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# by @KhurramRana on GitHub https://github.com/pytube/pytube/issues/1973#issuecomment-2232907131 (400 error fix)
# Adjust client versions for YouTube API requests
_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


# by @KhurramRana on GitHub https://github.com/pytube/pytube/issues/1973#issuecomment-2232907131 (400 error fix)
# Override the throttling function in pytube's cipher module
def get_throttling_function_name(js: str) -> str:
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )


cipher.get_throttling_function_name = get_throttling_function_name


# YouTube Downloader Application Class
class YouTubeDownloaderApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("720x480")
        self.root.title("YouTube Downloader")

        self.create_widgets()

    def create_widgets(self):
        """Create and arrange the UI components using pack."""
        self.title_label = ctk.CTkLabel(self.root, text="YouTube Downloader", font=("Arial", 24))
        self.title_label.pack(pady=10)

        self.url_label = ctk.CTkLabel(self.root, text="Enter the URL of the video you want to download:",
                                      font=("Arial", 18))
        self.url_label.pack(pady=5)

        self.url_var = ctk.StringVar()
        self.url_entry = ctk.CTkEntry(self.root, font=("Arial", 18), width=350, textvariable=self.url_var)
        self.url_entry.pack(pady=5)

        self.progress_label = ctk.CTkLabel(self.root, text="0%", font=("Arial", 18))
        self.progress_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.root, width=350, height=20)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5)

        self.download_button = ctk.CTkButton(self.root, text="Download", font=("Arial", 18),
                                             command=self.start_download)
        self.download_button.pack(pady=10)

        self.finished_label = ctk.CTkLabel(self.root, text="", font=("Arial", 18))
        self.finished_label.pack(pady=10)

    def start_download(self):
        """Start the download process in a separate thread."""
        url = self.url_var.get()
        if not self.validate_url(url):
            return

        self.progress_bar.set(0)
        self.progress_label.configure(text="0%")
        self.download_button.configure(state="disabled")
        download_thread = threading.Thread(target=self.download_video, args=(url,))
        download_thread.start()

    def validate_url(self, url):
        """
        Validate the URL to ensure it's a YouTube link.

        :param url: The URL to validate

        :return: True if the URL is valid, False otherwise
        """
        if not url:
            CTkMessagebox(title="Input Error", message="Please enter a YouTube URL.", icon="cancel", sound=True)
            return False
        if "youtube.com/watch?v=" not in url:
            CTkMessagebox(title="Input Error", message="Please enter a valid YouTube video URL.", icon="cancel",
                          sound=True)
            return False
        return True

    def download_video(self, url):
        """
        Download the YouTube video.

        :param url: The URL of the video to download
        """
        self.finished_label.configure(text="Downloading...", text_color="blue")
        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)
            stream = yt.streams.get_highest_resolution()
            stream.download()
            self.finished_label.configure(text="Finished Downloading", text_color="green")
        except Exception as e:
            self.finished_label.configure(text="Download Failed", text_color="red")
            logging.error(f"Error: {e}")  # Log the exception for debugging
        finally:
            self.download_button.configure(state="normal")

    def on_progress(self, stream, chunk, bytes_remaining):
        """
        Update progress bar and label during download.

        :param stream: The stream being downloaded
        :param chunk: The chunk of data being downloaded
        :param bytes_remaining: The number of bytes remaining to download
        """
        progress = (1 - bytes_remaining / stream.filesize) * 100
        self.progress_bar.set(progress / 100)
        self.progress_label.configure(text=f"{progress:.2f}%")


# Main function to run the application
if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.root.mainloop()
