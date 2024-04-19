import os
import bpy
import csv
import math
import random

COPIO = 1
OLIGO = 2
SPHY = 3
MPHY = 4
HEALTHY = [1, 2]
SENESCENT = 3
DEAD = 4
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
# Remove all particle objects
for obj in bpy.data.objects:
    if obj.name.startswith("particle"):
        if obj.animation_data is not None:
            bpy.data.actions.remove(obj.animation_data.action)
            obj.animation_data_clear()

scene = bpy.context.scene


def load_data_from_csv(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(
            file,
            fieldnames=FIELDNAMES,
            delimiter=",",
        )
        data = []
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


def check_for_attached_particles(particles):
    particles = particles.copy()
    attached_particles = []
    for particle in particles:
        for other_particle in particles:
            if (
                particle["id"] != other_particle["id"]
                and particle["x"] == other_particle["x"]
                and particle["y"] == other_particle["y"]
                and particle["z"] == other_particle["z"]
                and particle not in attached_particles
                and particle["species_id"] == COPIO
            ):
                attached_particles.append(particle)
    return attached_particles


def calc_bacteria_transformations(attached_particles, transformations):
    # add a small offset to improve visibility
    radius = MPHY_RADIUS + 0.005
    for particle in attached_particles:
        if particle["id"] not in [
            transformation["id"] for transformation in transformations
        ]:
            random_vector = generate_random_vector(radius)
            transformations.append(
                {
                    "id": particle["id"],
                    "x": random_vector[0],
                    "y": random_vector[1],
                    "z": random_vector[2],
                }
            )
            print("adding transformation for particle " + particle["id"])
    return transformations


def generate_random_vector(radius):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(-1, 1)
    length = math.sqrt(x**2 + y**2 + z**2)
    normalized_x = radius * x / length
    normalized_y = radius * y / length
    normalized_z = radius * z / length
    return (normalized_x, normalized_y, normalized_z)


def update_sphere(particle, sphere, transformations, frame):
    bsdf = None
    for transformation in transformations:
        if transformation["id"] == particle["id"]:
            particle["x"] += transformation["x"]
            particle["y"] += transformation["y"]
            particle["z"] += transformation["z"]
    bsdf = sphere.active_material.node_tree.nodes["Principled BSDF"]
    sphere.location = [particle["x"], particle["y"], particle["z"]]
    sphere.keyframe_insert(data_path="location")
    if particle["lifecycle_stage"] in HEALTHY:
        bsdf.inputs["Emission Strength"].default_value = 0.5
        bsdf.inputs["Emission Strength"].keyframe_insert(
            data_path="default_value")
    elif particle["lifecycle_stage"] == SENESCENT:
        bsdf.inputs["Emission Strength"].default_value = 0.2
        bsdf.inputs["Emission Strength"].keyframe_insert(
            data_path="default_value")
    elif particle["lifecycle_stage"] == DEAD:
        bsdf.inputs["Emission Strength"].default_value = 0.075
        bsdf.inputs["Emission Strength"].keyframe_insert(
            data_path="default_value")
    if sphere.hide_render:
        sphere.hide_render = False
        sphere.keyframe_insert(data_path="hide_render")
        sphere.hide_viewport = False
        sphere.keyframe_insert(data_path="hide_viewport")


frame = 1
file_path = os.environ["DATA_LOCATION"] + \
    "particles/particles-" + str(frame) + ".csv"
transformations = []
while os.path.exists(file_path):
    print("loading " + file_path)
    scene.frame_set(frame)
    data = load_data_from_csv(file_path)
    particle_names = set()
    attached_particles = check_for_attached_particles(data)
    # remove transformation if particle is not attached anymore in current timestep
    for particle in transformations:
        if particle["id"] not in [
            attached_particle["id"] for attached_particle in attached_particles
        ]:
            transformations.remove(particle)
            print("removing transformation for particle " + particle["id"])
    transformations = calc_bacteria_transformations(
        attached_particles, transformations)
    for row in data:
        particle_name = "particle-" + row["id"]
        particle_names.add(particle_name)
        sphere = bpy.data.objects[particle_name]
        if sphere:
            update_sphere(row, sphere, transformations, frame)
    for sphere in bpy.data.objects:
        if sphere.name.startswith("particle"):
            sphere.hide_render = False
            sphere.keyframe_insert(data_path="hide_render")
            sphere.hide_viewport = False
            sphere.keyframe_insert(data_path="hide_viewport")
            if sphere.name not in particle_names and not sphere.hide_render:
                sphere.hide_render = True
                sphere.keyframe_insert(data_path="hide_render")
                sphere.hide_viewport = True
                sphere.keyframe_insert(data_path="hide_viewport")
    frame += 1
    file_path = (
        os.environ["DATA_LOCATION"] +
        "particles/particles-" + str(frame) + ".csv"
    )
