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
import bpy
from .YT2B_Download import YT2B_Download

bl_info = {
    "name": "Youtube to Blender",
    "blender": (3,4,1),
    "category": "Import-Export",
    "version": (1,0),
    "description": "Download youtube audio directly into the blender video sequencer",
    "location": "SEQUENCE_EDITOR > Properties tab"
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
        channel = bpy.context.scene.yt2b_channel
        if channel < 1 or channel > 128:
            channel = 1
        url = bpy.context.scene.yt2b_url
        fileName, status = YT2B_Download(url)
        
        if status == "DOWNLOADED": # add to vse if a new file was downloaded
            # add sound strip to VSE
            if not context.scene.sequence_editor:
                context.scene.sequence_editor_create()
            
            soundStrip = context.scene.sequence_editor.sequences.new_sound(url, 
            fileName, channel,1)

        elif status == "YT2B_FILE_EXISTS":
            # check if strip is already in VSE
            found_strip = False
            for strip in bpy.context.scene.sequence_editor.sequences:
                if strip.name == url:
                    found_strip = True
                    break
            if found_strip == False:
                # add sound strip to VSE
                if not context.scene.sequence_editor:
                    context.scene.sequence_editor_create()
                
                soundStrip = context.scene.sequence_editor.sequences.new_sound(url, 
                fileName, channel,1)
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
        
        self.layout.operator("file.yt2b", text = "Download Audio",
        icon = "IMPORT")

def register():

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
