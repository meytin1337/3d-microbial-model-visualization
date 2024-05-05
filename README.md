# 3D visualization of a Microscale Microbial Ecology Model

This repository contains scripts to produce a 3D visualization of a Microscale Microbial Ecology Model in Blender.


## Producing a Movie


The video below is a tutorial on how to create a movie using the scripts.

https://github.com/meytin1337/3d-microbial-model-visualization/assets/15246633/7a6613c0-5b54-458d-885d-98df880c17d8

The scripts need to be run in Blender. They have to be copied to Blender's **scripts** tab.
The dataset needs to be placed into the `data` folder. An example dataset can be found under `data/example`.
All scripts have to be run with the `DATA_LOCATION` environment variable set to the data folder location. From a bash shell you can simply run `DATA_LOCATION=/path/to/data/folder blender`

## Updating the thresholds for coloring regions with increased DOM

For different datasets the distribution of DOM concentrations will vary and so the thresholds for coloring regions with increased DOM concentrations need to be adjusted.
The video below is a tutorial on how to adjust these thresholds.

https://github.com/meytin1337/3d-microbial-model-visualization/assets/15246633/6444ef13-f9d2-43cd-9ea8-854510ff3fc7

## Overview of the Scripts

#### Csv to OpenVDB

The script `src/grid/csv-to-openvdb.py` is used to transform the grid data to the openVDB data format. It can be run 

#### Import OpenVDB

The script `src/grid/import-openvdb.py` is used to import the openVDB data into Blender.


#### Create Particles

The script `src/particles/create-particles.py` is used to create spheres in Blender representing the particles in the dataset.

#### Update Particles

The script `src/particles/update-particles.py` is used to update the particles position and color in each timestep.

#### Camera Scripts

The scripts in `src/camera/` are used to update the camera type and location of the scene.

#### Shell Scripts

The scripts in `src/scripts/` are basic shellscripts to convert the output format from the model to the format required by the scripts.
