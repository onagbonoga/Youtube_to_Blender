import os
import subprocess
import ensurepip
import sys
import site
ensurepip.bootstrap()
pybin = sys.executable

user_site_dir = site.USER_SITE
cmd = [pybin, "-m", "pip", "install", "--user", "pytube"]
# Run the pip command in a shell
subprocess.run(cmd, check=True)
# add user site to path
sys.path.append(user_site_dir)

import pytube

def YT2B_Download(url):
    '''
    Download audio from youtube video 
    :param url - URL of video to be downloaded. This has to be a youtube url 
    '''
    try:
        yt = pytube.YouTube(url)
    except:
        print(f'Video {url} is unable to be downloaded')
        return " ", "YT2B_UNABLE_TO_DOWNLOAD"
    
    home_dir = os.path.expanduser("~")
    downloads_dir = os.path.join(home_dir, "Downloads")
    folderName = os.path.join(downloads_dir, "yt2BlenderDownloads")
    fileName = os.path.join(folderName, yt.title + ".mp3")

    if os.path.isfile(fileName):
        print("file already exists")
        return fileName, "YT2B_FILE_EXISTS"
    
    else:
        # extract only audio and download the file
        out_file = yt.streams.filter(only_audio=True).first().download(folderName)
        print(out_file)
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        
        os.rename(out_file, new_file)
        return fileName, "DOWNLOADED"
    
    
        