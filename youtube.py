import os
import yt_dlp

# Clear Screen
os.system("clear")

# Main Menu
print("Select Mode:")
print("1. Audio Only")
print("2. Single Video")
print("3. Playlist Download")
mode = input("\nEnter choice (1, 2 or 3): ")

# Ask for URL
url = input("\nEnter YouTube URL: ")

# Download folder
download_folder = "/sdcard/Download"

# Common options
def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\rDownloading: {d['_percent_str']} at {d.get('_speed_str','')} ETA {d.get('_eta_str','')}", end='')
    elif d['status'] == 'finished':
        print("\n✅ Download Finished! Processing...")

# Show Thumbnail
def show_thumbnail(info):
    thumb = info.get('thumbnail')
    if thumb:
        print(f"\nThumbnail Preview: {thumb}\n")

# Get info
with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
    info = ydl.extract_info(url, download=False)
    show_thumbnail(info)
    formats = info.get('formats', [])

# Mode 1: Audio Only
if mode == "1":
    os.system("clear")
    print("Audio Only Mode Selected.\n")
    print("Select Audio Quality:")
    print("1. 128 kbps")
    print("2. 192 kbps")
    print("3. 320 kbps")
    aq_choice = input("\nEnter choice: ")
    aq = "128" if aq_choice == "1" else "192" if aq_choice == "2" else "320"

    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': aq}],
        'progress_hooks': [progress_hook]
    }

    print("\nDownloading audio...")
    with yt_dlp.YoutubeDL(audio_opts) as ydl:
        ydl.download([url])
    print("\n✅ Audio Download Complete! Saved to Download folder.")

# Mode 2: Single Video
elif mode == "2":
    os.system("clear")
    print("Single Video Mode Selected.\nFetching formats...\n")

    video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('height')]
    print("Available Qualities:")
    quality_map = {}
    count = 1
    for f in video_formats:
        height = f.get('height', 'N/A')
        fps = f.get('fps', 30)
        format_id = f['format_id']
        print(f"{count}. {height}p{fps if fps > 30 else ''}")
        quality_map[count] = format_id
        count += 1

    choice = int(input("\nSelect Quality (number): "))
    selected_format = quality_map.get(choice)

    video_opts = {
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
        'format': selected_format,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook]
    }

    print("\nDownloading video, please wait...")
    with yt_dlp.YoutubeDL(video_opts) as ydl:
        ydl.download([url])
    print("\n✅ Video Download Complete! Saved to Download folder.")

# Mode 3: Playlist Download
elif mode == "3":
    os.system("clear")
    print("Playlist Mode Selected.\nFetching playlist info...\n")

    # Show title of playlist
    print(f"Playlist: {info.get('title','Unknown Playlist')}")

    # Select quality for all videos
    print("\nSelect Playlist Video Quality:")
    print("1. 360p")
    print("2. 720p")
    print("3. 1080p")
    print("4. Best Available")
    pq_choice = input("\nEnter choice: ")

    if pq_choice == "1":
        pq = "bestvideo[height<=360]+bestaudio/best"
    elif pq_choice == "2":
        pq = "bestvideo[height<=720]+bestaudio/best"
    elif pq_choice == "3":
        pq = "bestvideo[height<=1080]+bestaudio/best"
    else:
        pq = "bestvideo+bestaudio/best"

    playlist_opts = {
        'outtmpl': f'{download_folder}/%(playlist)s/%(title)s.%(ext)s',
        'format': pq,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook]
    }

    print("\nDownloading playlist, this may take time...")
    with yt_dlp.YoutubeDL(playlist_opts) as ydl:
        ydl.download([url])
    print("\n✅ Playlist Download Complete! Saved to Download folder.")

else:
    print("Invalid choice. Please run again.")
