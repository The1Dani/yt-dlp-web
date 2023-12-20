from flask import Flask
from flask import redirect, render_template, request
import os
import configparser

import yt_dlp

#? Config File init

config = configparser.ConfigParser()

if not os.path.isfile(r"config.ini"):
    config.add_section("Paths")
    config.set("Paths","videos","Replace This")
    config.set("Paths","audio","Replace This")
    config.add_section("Quality")
    config.set("Quality","max-height","1080")
    with open(r"config.ini", "w") as configfile:
        config.write(configfile)

app = Flask(__name__)

config.read("config.ini")

#?
paths = config["Paths"]
videos_path = paths["videos"]
audio_path = paths["audio"]
set_quality = config["Quality"]["max-height"]

#?

def isValidPath():
    if os.path.isdir(videos_path) and os.path.isdir(audio_path):
        return True
    else: 
        return False

if os.path.isdir(videos_path) and os.path.isdir(audio_path):

    ydl_opts_vid = {
        'format': f"bestvideo[height<={set_quality}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "paths": {
            "home": videos_path 
        }
    }

    ydl_opts_aud = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{  
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }],
        "paths": {
            "home": audio_path 
        }
    }

    def ytdwn(URL,ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(URL)
            if error_code:
                return error_code
            

    @app.route("/", methods=["GET","POST"])
    def hello_world():

        if request.method == "POST":
            URL = request.form.get("url")
            checkbox = request.form.get("checkbox") # on/mp3 off/mp4

            if not URL:
                return redirect("/")
            else:
                if checkbox == "on":
                    err = ytdwn(URL,ydl_opts_aud)
                    
                else:
                    err = ytdwn(URL,ydl_opts_vid)
                    

                if err:
                    print(err)
                    
                return redirect("/")
        else:
            return render_template("base.html")

else:
    print(videos_path,"asd")
    print("Put in a valid dir for both video and audio in the config.ini")
    
