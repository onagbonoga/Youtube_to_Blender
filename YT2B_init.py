import bpy
import os

#####################MOVE TO SEPERATE FILE

def YT2B_Download(url):
    from pytube import YouTube
    # enter URL here
    #url = "https://www.youtube.com/watch?v=dD8QWwPKuhU"

    # url input from user
    try:
        yt = YouTube(url)
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
####################################

bl_info = {
    "name": "Youtube to Blender",
    "blender": (3,4,1),
    "category": "Import-Export",
}

# define operator for YT2B functionality
class YT2B_OT_function(bpy.types.Operator):
    '''Install youtube audio into blender VSE'''
    bl_idname = "file.yt2b"
    bl_label = "youtube to blender"
    bl_options = {'REGISTER'}
    
    video_url: bpy.props.StringProperty(
    name = "video_url",
    description = "url for the video you wish to download",
    )
    
    def execute(self, context): # runs when called
        # download sound strip
        fileName = YT2B_Download(bpy.context.scene.yt2b_url)
        channel = bpy.context.scene.yt2b_channel
        if channel < 1 or channel > 128:
            channel = 3
        print(fileName)
        
        # add sound strip to VSE
        if not context.scene.sequence_editor:
            context.scene.sequence_editor_create()
        
        soundStrip = context.scene.sequence_editor.sequences.new_sound(fileName, 
        fileName, channel,1)
        return {'FINISHED'}
        
# define the panel for the addon 
class YT2B_PT_view(bpy.types.Panel):
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "YT2B"
    bl_label = "Download Youtube Audio"
    
    def draw(self, context):
        row = self.layout.row()
        row.label(text="Enter Video URL Below:")
        row = self.layout.row()
        row.prop(context.scene, "yt2b_url")
        
        row = self.layout.row()
        row.label(text="Enter Sequence Channel Number:")
        row = self.layout.row()
        row.prop(context.scene, "yt2b_channel")
        
        self.layout.operator("file.yt2b", text = "Download Audio",
        icon = "IMPORT")

def register():
    # install pytube
    import subprocess
    import ensurepip
    import sys
    ensurepip.bootstrap()
    pybin = sys.executable
    #subprocess.check_call([pybin, '-m', 'pip', 'install', 'pytube'])
    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"
    subprocess.run([sys.executable, "-m", "pip", "install", "pytube", "--user"]
    , check=True, env=environ_copy)
    
    # register custom property to accept user input as URL
    bpy.types.Scene.yt2b_url = bpy.props.StringProperty(name="")
    bpy.types.Scene.yt2b_channel = bpy.props.IntProperty(name="")
    
    # register operator and panel for the addon
    bpy.utils.register_class(YT2B_OT_function)
    bpy.utils.register_class(YT2B_PT_view)

def unregister():
    # register operator and panel for the addon
    bpy.utils.unregister_class(YT2B_OT_function)
    bpy.utils.unregister_class(YT2B_PT_view)
    print("Thank you for using Youtube to Blender!")


# delete in final version   
if __name__ == "__main__":
    register()