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
        has_audio = "✅Audio" if f.get('acodec') != 'none' else "❌No Audio (Mergeable)"
        print(f"{count}. {height}p{fps if fps > 30 else ''} [{has_audio}]")
        quality_map[count] = format_id
        count += 1

    choice = int(input("\nSelect Quality (number): "))
    selected_format = quality_map.get(choice)

    # Use merge if audio missing
    video_opts = {
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
        'format': f'{selected_format}+bestaudio/best',  # Merge video + best audio
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

    print(f"Playlist: {info.get('title','Unknown Playlist')}\n")
    entries = info.get('entries', [])

    # Check first video formats for available qualities
    if entries:
        first_video_formats = entries[0].get('formats', [])
        print("Available Qualities (with audio info from first video):")
        quality_map = {}
        count = 1
        for f in first_video_formats:
            if f.get('vcodec') == 'none' or not f.get('height'):
                continue
            height = f.get('height', 'N/A')
            fps = f.get('fps', 30)
            format_id = f['format_id']
            has_audio = "✅Audio" if f.get('acodec') != 'none' else "❌No Audio (Mergeable)"
            print(f"{count}. {height}p{fps if fps > 30 else ''} [{has_audio}]")
            quality_map[count] = format_id
            count += 1

        choice = int(input("\nSelect Quality (number) for all videos: "))
        selected_format = quality_map.get(choice)

        playlist_opts = {
            'outtmpl': f'{download_folder}/%(playlist)s/%(title)s.%(ext)s',
            'format': f'{selected_format}+bestaudio/best',  # Merge video + best audio
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook]
        }

        print("\nDownloading playlist, this may take time...")
        with yt_dlp.YoutubeDL(playlist_opts) as ydl:
            ydl.download([url])
        print("\n✅ Playlist Download Complete! Saved to Download folder.")
    else:
        print("❌ No videos found in playlist.")

else:
    print("Invalid choice. Please run again.")
