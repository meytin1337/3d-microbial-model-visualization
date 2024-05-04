import os
import bpy

# Remove all grid objects
for obj in bpy.data.objects:
    if obj.name.startswith("grid-"):
        if obj.animation_data is not None:
            bpy.data.actions.remove(obj.animation_data.action)
            obj.animation_data_clear()
        bpy.data.objects.remove(obj, do_unlink=True)


material = bpy.data.materials.new(name="VolumeShader")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

for node in nodes:
    nodes.remove(node)

output_node = nodes.new(type="ShaderNodeOutputMaterial")
volume_node = nodes.new(type="ShaderNodeVolumePrincipled")
volume_info_node = nodes.new(type="ShaderNodeVolumeInfo")
color_ramp_node = nodes.new(type="ShaderNodeValToRGB")

color_ramp_node.color_ramp.interpolation = "CONSTANT"
color_ramp_elements = color_ramp_node.color_ramp.elements
# these values work with the example data
# but would need to be adjusted for other data
new_element = color_ramp_elements.new(0.22)
new_element.color = (0.32, 0.166, 0, 1.0)
color_ramp_elements[2].color = (0.35, 0.087, 0, 1.0)
color_ramp_elements[2].position = 0.27

volume_node.inputs["Density"].default_value = 0.0

links.new(volume_info_node.outputs["Density"], color_ramp_node.inputs["Fac"])
links.new(color_ramp_node.outputs["Color"],
          volume_node.inputs["Emission Strength"])
links.new(color_ramp_node.outputs["Color"],
          volume_node.inputs["Emission Color"])
links.new(volume_node.outputs["Volume"], output_node.inputs["Volume"])
links.new(volume_node.outputs["Volume"], output_node.inputs["Volume"])


def create_grid(file_path, i):
    bpy.ops.object.volume_import(filepath=file_path, files=[])
    obj = bpy.data.objects["grid-" + str(i)]
    obj.data.materials.append(material)
    obj.hide_set(True)
    create_frame(i)


def create_frame(i):
    scene = bpy.context.scene
    scene.frame_set(i)
    for obj in bpy.data.objects:
        if obj.name.startswith("grid-"):
            if obj.name == "grid-" + str(i) and obj.hide_render:
                obj.hide_render = False
                obj.keyframe_insert(data_path="hide_render")
            else:
                obj.hide_render = True
                obj.keyframe_insert(data_path="hide_render")


index = 1
file_path = os.environ['DATA_LOCATION'] + "grid/grid-" + str(index) + ".vdb"
while os.path.exists(file_path):
    print('loading ' + file_path)
    create_grid(file_path, index)
    index += 1
    file_path = os.environ['DATA_LOCATION'] + "grid/grid-" + str(index) + ".vdb"


frame = 1
while frame < index:
    create_frame(frame)
    frame += 1
