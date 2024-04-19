import csv
import os
import numpy as np
import pyopenvdb as openvdb
import math

FIELDNAMES = [
    "_timestep",
    "box_id_x",
    "box_id_y",
    "box_id_z",
    "_x_center",
    "_y_center",
    "_z_center",
    "concentration",
]


def load_volume(file_path, highest_concentration, lowest_concentration):
    Volume = np.zeros([56, 56, 56])
    with open(file_path, "r") as file:
        reader = csv.DictReader(
            file,
            fieldnames=FIELDNAMES,
            delimiter=",",
        )
        for row in reader:
            row = cast_fields(row)
            Volume[row["box_id_x"] - 1, row["box_id_y"] - 1, row["box_id_z"] - 1] = (
                transform_concentration(
                    row["concentration"], highest_concentration, lowest_concentration
                )
            )
    return Volume


def cast_fields(fields):
    fields["box_id_x"] = int(fields["box_id_x"])
    fields["box_id_y"] = int(fields["box_id_y"])
    fields["box_id_z"] = int(fields["box_id_z"])
    fields["concentration"] = float(fields["concentration"])
    return fields


# all values are between 0 and 1 with log10 scaling


def transform_concentration(concentration, highest_concentration, lowest_concentration):
    return (math.log10(concentration / lowest_concentration)) / (
        math.log10(highest_concentration / lowest_concentration)
    )


def create_grid(Volume, i):
    grid = openvdb.FloatGrid()
    grid.copyFromArray(Volume.astype(float))
    # transform the grid to be 14x14x14 instead of 56x56x56
    grid.transform = openvdb.createLinearTransform(
        [[0.25, 0, 0, 0], [0, 0.25, 0, 0], [0, 0, 0.25, 0], [0, 0, 0, 1]]
    )
    grid.gridClass = openvdb.GridClass.FOG_VOLUME
    grid.name = "density"
    openvdb.write(os.environ['DATA_LOCATION'] + "grid-" + i + ".vdb", grid)


file_path = os.environ['DATA_LOCATION'] + "grid-1.csv"
i = 1
j = 1
highest_concentration = 0
lowest_concentration = 100000
# find highest and lowest concentration across all files
while os.path.exists(file_path):
    with open(file_path, "r") as file:
        reader = csv.DictReader(
            file,
            fieldnames=FIELDNAMES,
            delimiter=",",
        )
        for row in reader:
            row = cast_fields(row)
            if row["concentration"] > highest_concentration:
                highest_concentration = row["concentration"]
            if row["concentration"] < lowest_concentration:
                lowest_concentration = row["concentration"]
    i += 1
    file_path = os.environ['DATA_LOCATION'] + "grid/grid-" + str(i) + ".csv"
    print(
        "highest_concentration: "
        + str(highest_concentration)
        + " lowest_concentration: "
        + str(lowest_concentration)
    )

file_path = os.environ['DATA_LOCATION'] + "grid/grid-1.csv"
while os.path.exists(file_path):
    print('loading ' + file_path)
    Volume = load_volume(file_path, highest_concentration,
                         lowest_concentration)
    create_grid(Volume, str(j))
    j += 1
    file_path = os.environ['DATA_LOCATION'] + "grid/grid-" + str(j) + ".csv"
