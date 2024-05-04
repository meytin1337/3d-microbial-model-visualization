import bpy
import math
import mathutils
import csv
import os

FIELDNAMES = [
    "_row_id",
    "id",
    "_species_id",
    "_lifecycle_stage",
    "x",
    "y",
    "z",
    "theta",
    "phi",
    "diameter",
]

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


def load_data_from_csv(file_path, frame):
    with open(file_path, "r") as file:
        reader = csv.DictReader(
            file,
            fieldnames=FIELDNAMES,
            delimiter=",",
        )
        for row in reader:
            # id should match the particle we want to "attach" the camera to
            if str(int(float(row["id"]))) == "60":
                print(row["theta"])
                create_frame(
                    float(row["theta"]),
                    float(row["phi"]),
                    (
                        float(row["x"]) * 0.01,
                        float(row["y"]) * 0.01,
                        float(row["z"]) * 0.01,
                    ),
                    float(row["diameter"]) * 0.01,
                    frame,
                )
                break


def create_frame(theta, phi, coordinates, diameter, frame):
    bpy.context.scene.frame_set(frame)
    # convert to cartesian coordinates
    x = diameter / 2 * math.sin(theta) * math.cos(phi)
    y = diameter / 2 * math.sin(theta) * math.sin(phi)
    z = diameter / 2 * math.cos(theta)

    # The desired direction vector
    direction = mathutils.Vector((x, y, z)).normalized()

    # Align the camera's -Z axis with the direction vector
    # The camera's up direction is assumed to be the global Y axis
    rotation_matrix = direction.to_track_quat("-Z", "Y")

    camera_object.rotation_euler = rotation_matrix.to_euler()
    bpy.context.view_layer.update()

    camera_object.location = coordinates
    camera_object.keyframe_insert(data_path="location", index=-1)
    camera_object.keyframe_insert(data_path="rotation_euler", index=-1)


file_path = os.environ["DATA_LOCATION"] + "/particles/particles-1.csv"
frame = 1
while os.path.exists(file_path):
    data = load_data_from_csv(file_path, frame)
    frame += 1
    file_path = os.environ["DATA_LOCATION"] + \
        "/particles/particles-" + str(frame) + ".csv"
    print("loading: " + file_path)
