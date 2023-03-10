import os
import bpy 
import subprocess
import ensurepip
import sys
ensurepip.bootstrap()
pybin = sys.executable
subprocess.check_call([pybin, '-m', 'pip', 'install', 'pytube'])
import importlib

importlib.import_module('pytube')
#from pytube import YouTube

def YT2B_Download(url):
    # url input from user
    try:
        yt = pytube.YouTube(url)
    except:
        print(f'Video {url} is unable to be downloaded')
        return "YT2B_UNABLE_TO_DOWNLOAD"
    fileName = bpy.path.abspath("//yt2BlenderDownloads//") + yt.title +".mp3"
    
    if not os.path.isfile(fileName):
        # extract only audio
        video = yt.streams.filter(only_audio=True).first()
        
        # download the file
        out_file = video.download(bpy.path.abspath("//yt2BlenderDownloads//"))
        print(out_file)
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        
        os.rename(out_file, new_file)
    
    else:
        print("file already exists")
    
    return fileName