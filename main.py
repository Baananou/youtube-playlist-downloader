from flask import Flask, request, jsonify
from pytube import YouTube, Playlist

app = Flask(__name__)


def download_playlist(url, download_type):
    playlist = Playlist(url)
    for video_url in playlist.video_urls:
        download_single_video(video_url, download_type)


def download_single_video(url, download_type):
    video = YouTube(url)
    stream = video.streams.get_audio_only(
    ) if download_type == 'mp3' else video.streams.get_highest_resolution()
    stream.download()
    print(f"Downloaded: {video.title}")


@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    download_type = data.get('download_type')
    download = data.get('download')

    if download_type not in ('mp3', 'mp4'):
        return jsonify({"error": "Invalid download type. Please choose 'mp3' or 'mp4'."}), 400

    if download == 'playlist':
        result = download_playlist(playlist_url, download_type)
        return jsonify(result), 200

    elif download == 'video':
        result = download_single_video(url, download_type)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Invalid download type. Please choose 'playlist' or 'video'."}), 400


if __name__ == "__main__":
    app.run(debug=True)

    # choice = input(
    #     "Enter 'playlist' to download a playlist or 'video' to download a single video: ")

    # if choice == 'playlist':
    #     playlist_url = input("Enter the playlist URL: ")
    #     download_type = input(
    #         "Enter 'mp3' to download as audio or 'mp4' to download as video: ")

    #     if download_type not in ('mp3', 'mp4'):
    #         print("Invalid download type. Please choose 'mp3' or 'mp4'.")
    #     else:
    #         download_playlist(playlist_url, download_type)
    #         print("Download completed!")

    # elif choice == 'video':
    #     video_url = input("Enter the video URL: ")
    #     download_type = input(
    #         "Enter 'mp3' to download as audio or 'mp4' to download as video: ")

    #     if download_type not in ('mp3', 'mp4'):
    #         print("Invalid download type. Please choose 'mp3' or 'mp4'.")
    #     else:
    #         download_single_video(video_url, download_type)
    #         print("Download completed!")

    # else:
    #     print("Invalid choice. Please enter 'playlist' or 'video'.")
