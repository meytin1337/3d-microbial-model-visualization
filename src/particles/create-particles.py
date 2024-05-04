import bpy
import csv
import os

COPIO = 1
OLIGO = 2
SPHY = 3
MPHY = 4
HEALTHY = [1, 2]
SENESCENT = 3
DEAD = 4
COPIO_RADIUS = 0.05
OLIGO_RADIUS = 0.025
SPHY_RADIUS = 0.05
MPHY_RADIUS = 0.2
FIELDNAMES = [
    "_row_id",
    "id",
    "species_id",
    "lifecycle_stage",
    "x",
    "y",
    "z",
    "theta",
    "phi",
    "_diameter",
]
# Clear all mesh objects
for obj in bpy.data.objects:
    if obj.name.startswith("particle"):
        if obj.animation_data is not None:
            bpy.data.actions.remove(obj.animation_data.action)
            obj.animation_data_clear()
        for slot in obj.material_slots:
            mat = slot.material
            if mat:
                bpy.data.materials.remove(mat)
        bpy.data.objects.remove(obj, do_unlink=True)

scene = bpy.context.scene


def load_data_from_csv(file_path):
    scene.frame_set(1)
    with open(file_path, "r") as file:
        data = []
        reader = csv.DictReader(
            file,
            fieldnames=FIELDNAMES,
            delimiter=",",
        )
        for row in reader:
            row["id"] = str(int(float(row["id"])))
            row["species_id"] = int(float(row["species_id"]))
            row["lifecycle_stage"] = int(float(row["lifecycle_stage"]))
            row["x"] = float(row["x"]) * 0.01
            row["y"] = float(row["y"]) * 0.01
            row["z"] = float(row["z"]) * 0.01
            row["theta"] = float(row["theta"])
            row["phi"] = float(row["phi"])
            data.append(row)
        return data


def create_sphere(fields):
    radius = None
    id = fields["id"]
    mat = bpy.data.materials.new(name="Material" + str(id))
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    for node in nodes:
        nodes.remove(node)
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.inputs["Emission Strength"].default_value = 0.5
    bsdf.inputs["Base Color"].default_value = (0, 0, 0, 1)
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    mat.node_tree.links.new(
        bsdf.outputs["BSDF"], output_node.inputs["Surface"])
    coordinates = [fields["x"], fields["y"], fields["z"]]
    if fields["species_id"] == COPIO:
        radius = COPIO_RADIUS
        bsdf.inputs["Emission Color"].default_value = (1, 0, 0, 1)
    elif fields["species_id"] == OLIGO:
        radius = OLIGO_RADIUS
        bsdf.inputs["Emission Color"].default_value = (0, 0.25, 1, 1)
    elif fields["species_id"] == SPHY:
        radius = SPHY_RADIUS
        bsdf.inputs["Emission Color"].default_value = (0, 1, 0.25, 1)
    elif fields["species_id"] == MPHY:
        radius = MPHY_RADIUS
        bsdf.inputs["Emission Color"].default_value = (0, 1, 0, 1)
    if fields["lifecycle_stage"] in HEALTHY:
        bsdf.inputs["Emission Strength"].default_value = 0.5
    elif fields["lifecycle_stage"] == SENESCENT:
        bsdf.inputs["Emission Strength"].default_value = 0.2
    elif fields["lifecycle_stage"] == DEAD:
        bsdf.inputs["Emission Strength"].default_value = 0.075
    bpy.ops.mesh.primitive_ico_sphere_add(location=coordinates, radius=radius)
    obj = bpy.context.active_object
    obj.name = "particle-" + str(id)
    obj.active_material = mat
    # smooth object
    obj.modifiers.new("Subdivision", type="SUBSURF")
    obj.modifiers["Subdivision"].levels = 2
    obj.modifiers["Subdivision"].render_levels = 2
    obj.keyframe_insert(data_path="location")
    for face in obj.data.polygons:
        face.use_smooth = True


frame = 1
file_path = os.environ['DATA_LOCATION'] + "/particles/particles-" + str(frame) + ".csv"
while os.path.exists(file_path):
    print('loading ' + file_path)
    scene.frame_set(frame)
    data = load_data_from_csv(file_path)
    for row in data:
        if "particle-" + str(row["id"]) not in bpy.data.objects:
            create_sphere(row)
    frame += 1
    file_path = os.environ['DATA_LOCATION'] + "/particles/particles-" + str(frame) + ".csv"
