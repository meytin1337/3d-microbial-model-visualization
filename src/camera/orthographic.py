import bpy
import math

for obj in bpy.data.objects:
    if obj.name.startswith("Camera"):
        if obj.animation_data is not None:
            bpy.data.actions.remove(obj.animation_data.action)
            obj.animation_data_clear()
        bpy.data.objects.remove(obj, do_unlink=True)

camera_data = bpy.data.cameras.new(name="Camera")
camera_object = bpy.data.objects.new("Camera", camera_data)
bpy.context.collection.objects.link(camera_object)
bpy.context.scene.camera = camera_object


camera = bpy.data.objects["Camera"]
camera.rotation_euler = (math.pi / 2, 0, -math.pi / 2)
camera.location = (0, 7, 7)
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 13.8
