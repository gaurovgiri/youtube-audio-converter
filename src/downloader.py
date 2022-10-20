import youtube_dl
from deta import Deta
from dotenv import dotenv_values 

config = dotenv_values(".env")

deta = Deta(config["PROJECT_KEY"])
database = deta.Base(config["BASE"])

def download_ytb2mp3():
    video_url = input("enter url of youtube video:")
    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
    filename = f"assets/audio/{video_info['id']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }
    
    if database.fetch({"id":video_info['id']}).count != 0:
        print("Already Downloaded")

    
    else:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
            print("Download complete... {}".format(filename))
        database.insert(video_info)

if __name__ == "__main__":
    download_ytb2mp3()
