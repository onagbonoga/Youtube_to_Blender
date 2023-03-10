'''
Copyright (C) 2023 Nurudeen Agbonoga

Created by Nurudeen Agbonoga

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Youtube to Blender",
    "blender": (3,4,1),
    "category": "Import-Export",
    "version": (1,0),
    "description": "Download youtube video or audio directly into the blender video sequencer",
    "location": "Video Sequence Editor > Properties tab"
}

import bpy
from .YT2B_Download import YT2B_Download

# define operator for YT2B audio download
class YT2B_OT_Download_Audio(bpy.types.Operator): 
    '''Download youtube audio into blender VSE'''
    bl_idname = "file.yt2b_audio"
    bl_label = "youtube to blender download audio"
    bl_options = {'REGISTER'}
    
    def execute(self, context): # runs when called
        # download sound strip
        channel = bpy.context.scene.yt2b_channel
        if channel < 1 or channel > 128:
            channel = 1
        url = bpy.context.scene.yt2b_url
        fileName, status = YT2B_Download(url, True)
        stripName = "A" + url
        
        if status == "YT2B_DOWNLOADED": # add to vse if a new file was downloaded
            # add sound strip to VSE
            if not context.scene.sequence_editor:
                context.scene.sequence_editor_create()
            
            context.scene.sequence_editor.sequences.new_sound(stripName, 
            fileName, channel,1)

        elif status == "YT2B_FILE_EXISTS":
            # check if strip is already in VSE
            found_strip = False
            for strip in bpy.context.scene.sequence_editor.sequences:
                if strip.name == stripName:
                    found_strip = True
                    break
            if found_strip == False:
                # add sound strip to VSE
                if not context.scene.sequence_editor:
                    context.scene.sequence_editor_create()
                
                context.scene.sequence_editor.sequences.new_sound(stripName, 
                    fileName, channel,1)
        elif status == "YT2B_UNABLE_TO_DOWNLOAD":
            print("was unable to download strip")
        return {'FINISHED'}
    
# define operator for YT2B video download
class YT2B_OT_Download_Video(bpy.types.Operator):
    '''Download youtube video into blender VSE'''
    bl_idname = "file.yt2b_video"
    bl_label = "youtube to blender download video"
    bl_options = {'REGISTER'}
    
    def execute(self, context): # runs when called
        # download audio strip
        channel = bpy.context.scene.yt2b_channel
        if channel < 1 or channel > 128:
            channel = 1
        url = bpy.context.scene.yt2b_url
        fileName, status = YT2B_Download(url, False)
        stripName = "V" + url
        
        if status == "YT2B_DOWNLOADED": # add to vse if a new file was downloaded
            # add sound strip to VSE
            if not context.scene.sequence_editor:
                context.scene.sequence_editor_create()
            
            #soundStrip = context.scene.sequence_editor.sequences.new_movie(stripName, 
            #fileName, channel,1)
            movie = bpy.ops.sequencer.movie_strip_add(filepath=fileName, 
                channel=channel, frame_start=1, sound=True)

        elif status == "YT2B_FILE_EXISTS":
            # check if strip is already in VSE
            found_strip = False
            
            for strip in bpy.context.scene.sequence_editor.sequences:
                if strip.name == stripName:
                    found_strip = True
                    break
            if found_strip == False:
                # add sound strip to VSE
                if not context.scene.sequence_editor:
                    context.scene.sequence_editor_create()
                
                movie = bpy.ops.sequencer.movie_strip_add(filepath=fileName, 
                channel=channel, frame_start=1, sound=True)
                      
                
        else:
            print("was unable to download strip")
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
        
        self.layout.operator("file.yt2b_audio", text = "Download only Audio",
        icon = "IMPORT")

        self.layout.operator("file.yt2b_video", text = "Download Video and Audio",
        icon = "IMPORT")

def register():

    # register custom property to accept user input as URL
    bpy.types.Scene.yt2b_url = bpy.props.StringProperty(name="")
    bpy.types.Scene.yt2b_channel = bpy.props.IntProperty(name="", default = 1)
    
    # register operator and panel for the addon
    bpy.utils.register_class(YT2B_OT_Download_Audio)
    bpy.utils.register_class(YT2B_OT_Download_Video)
    bpy.utils.register_class(YT2B_PT_view)

def unregister():
    # register operator and panel for the addon
    bpy.utils.unregister_class(YT2B_OT_Download_Audio)
    bpy.utils.unregister_class(YT2B_OT_Download_Video)
    bpy.utils.unregister_class(YT2B_PT_view)
    print("Thank you for using Youtube to Blender!")
