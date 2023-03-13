import os
import subprocess
import ensurepip
import sys
import site

# import pytube module
ensurepip.bootstrap()
pybin = sys.executable
user_site_dir = site.USER_SITE
cmd = [pybin, "-m", "pip", "install", "--user", "pytube"]

# Run the pip command in a shell
subprocess.run(cmd, check=True)

# add user site to path. This is so blenders version of python can access user modules
sys.path.append(user_site_dir)

import pytube

def clean_up_title(title):
    '''
    This functions removes special characters from youtube titles
    '''
    chars_to_remove = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    
    for char in chars_to_remove:
        title = title.replace(char, '')
    
    return title

    
def YT2B_Download(url, onlyAudio):
    '''
    Download audio from youtube video 
    :param url: URL of video to be downloaded. This has to be a youtube url 
    :returns: File name of the youtube video to be downloaded and the status 
        which can be "YT2B_UNABLE_TO_DOWNLOAD", "YT2B_FILE_EXISTS" 
        or "YT2B_DOWNLOADED"
    :rtype: tuple 
    '''
    
    try:
        yt = pytube.YouTube(url)
    except:
        print(f'Video {url} is unable to be downloaded')
        return " ", "YT2B_UNABLE_TO_DOWNLOAD"
    
    home_dir = os.path.expanduser("~")
    downloads_dir = os.path.join(home_dir, "Downloads")
    folderName = os.path.join(downloads_dir, "yt2BlenderDownloads")
    
    if onlyAudio:
        title = clean_up_title(yt.title)
        fileName = os.path.join(folderName, "A" + title + ".mp3")

        if os.path.isfile(fileName):
            print("file already exists")
            return fileName, "YT2B_FILE_EXISTS"
        
        else:
            # extract only audio and download the file
            out_file = yt.streams.filter(only_audio=True).first().download(folderName)
            # save the file
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
    
    else: # downlaod video and audio
        title = clean_up_title(yt.title)
        fileName = os.path.join(folderName, "V" + title + ".mp4")

        if os.path.isfile(fileName):
            print("file already exists")
            return fileName, "YT2B_FILE_EXISTS"
        
        else:
            out_file = yt.streams.get_highest_resolution().download(folderName)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
        

        
    os.rename(out_file, fileName)
    return fileName, "YT2B_DOWNLOADED"
