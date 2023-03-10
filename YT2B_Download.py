import os
import bpy 
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

'''def import_module(module_name):
    """
    import a module and assign it to a globals dictionary
    :param module: the module to be imported
    """
    globals()[module_name] = importlib.import_module(module_name)
    

def install_pip():
    """
    Installs pip if not already present. Please note that ensurepip.bootstrap() also calls pip, which adds the
    environment variable PIP_REQ_TRACKER. After ensurepip.bootstrap() finishes execution, the directory doesn't exist
    anymore. However, when subprocess is used to call pip, in order to install a package, the environment variables
    still contain PIP_REQ_TRACKER with the now nonexistent path. This is a problem since pip checks if PIP_REQ_TRACKER
    is set and if it is, attempts to use it as temp directory. This would result in an error because the
    directory can't be found. Therefore, PIP_REQ_TRACKER needs to be removed from environment variables.
    :return:
    """

    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)

def install_and_import_module(module_name):
    """
    Installs the package through pip and attempts to import the installed module
    """
    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    subprocess.run([sys.executable, "-m", "pip", "install", module_name, "--user"], check=True, env=environ_copy)

    # The installation succeeded, attempt to import the module again
    import_module(module_name)

try:
    install_pip()
    install_and_import_module("pytube")
    print(">>>>>>>>>>>>>Module imported successfully!")

except (subprocess.CalledProcessError, ImportError) as err:
        print("unable to import modules")'''

import pytube

def YT2B_Download(url):
    # url input from user
    #yt = pytube.YouTube(url)
    try:
        yt = pytube.YouTube(url)
    except:
        print(f'Video {url} is unable to be downloaded')
        return "YT2B_UNABLE_TO_DOWNLOAD"
    #fileName = bpy.path.abspath("//yt2BlenderDownloads//") + yt.title +".mp3"
    home_dir = os.path.expanduser("~")
    downloads_dir = os.path.join(home_dir, "Downloads")
    folderName = os.path.join(downloads_dir, "yt2BlenderDownloads")
    fileName = os.path.join(folderName, yt.title + ".mp3")

    if not os.path.isfile(fileName):
        # extract only audio
        #video = yt.streams.filter(only_audio=True).first()
        
        # download the file
        #out_file = video.download(folderName)
        out_file = yt.streams.filter(only_audio=True).first().download(folderName)
        print(out_file)
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        
        os.rename(out_file, new_file)
        return fileName
    
    else:
        print("file already exists")
        return "YT2B_FILE_EXISTS"