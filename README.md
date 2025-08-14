# smart-youtube-downloader
A Termux-based smart YouTube downloader with video, audio, and playlist support.

# Smart YouTube Downloader (Termux Version)

A powerful Termux-based YouTube downloader that supports:

✅ Video download with quality selection

✅ Audio-only download with quality selection

✅ Full Playlist download with custom quality

✅ Auto-save files into the Download folder



---

Features

🎥 Video Download – Choose from multiple resolutions (144p up to 4K).

🎵 Audio Only – Download high-quality audio (mp3/m4a).

📂 Playlist Support – Download entire playlists in your chosen quality.

🧾 Interactive Menu – Easy-to-use interface with numbered options.

🔍 Format Selection – Displays all available formats before download.

---

Installation (Termux)

1. Update Termux and install Python

pkg update && pkg upgrade -y
pkg install python -y
pkg install git -y

2. Install Required Python Packages

pip install yt-dlp

---

Clone Repository

git clone https://github.com/Madushakelum/smart-youtube-downloader.git
cd smart-youtube-downloader

---

Run the Script

python youtube.py


---

Usage

When you run the script:

1. Main Menu appears:

1️⃣ Video Download

2️⃣ Audio Only

3️⃣ Playlist Download

0️⃣ Exit



2. Enter the option number.


3. Paste the YouTube URL.


4. Choose the quality by typing the number.


5. Download will start automatically in Download folder.

6. Example Output

Enter URL: https://youtube.com/watch?v=example
Select format:
1. 144p
2. 240p
3. 360p
4. 480p
5. 720p
6. 1080p
7. Audio 128kbps
8. Audio 256kbps


---

License

This project is licensed under the MIT License.
