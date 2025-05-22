import yt_dlp
from yt_dlp.utils import DownloadError
from deta import Deta
from dotenv import dotenv_values 

config = dotenv_values(".env")

deta = Deta(config["PROJECT_KEY"])
database = deta.Base(config["BASE"])

def download_ytb2mp3():
    try:
        video_url = input("enter url of youtube video:")
        video_info = yt_dlp.YoutubeDL().extract_info(url = video_url,download=False)
        db_entry = {
            'id': video_info['id'],
        'title': video_info['title'],
        'webpage_url': video_info['webpage_url'],
        'audio_format': 'mp3',
        'audio_quality': '192kbps'
    }
    filename = f"assets/audio/{video_info['id']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    if database.fetch({"id":video_info['id']}).count != 0:
        print("Already Downloaded")

    
    else:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
            print("Download complete... {}".format(filename))
        database.insert(db_entry)
    except DownloadError as e:
        print(f"Error during download: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    download_ytb2mp3()
