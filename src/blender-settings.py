import bpy
import os

bpy.ops.object.select_all(action='SELECT')

bpy.ops.object.delete()

bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.render.resolution_percentage = 100

bpy.context.scene.render.image_settings.file_format = 'FFMPEG'

bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

bpy.context.scene.render.filepath = os.environ['DATA_LOCATION'] + "/../../output/"
