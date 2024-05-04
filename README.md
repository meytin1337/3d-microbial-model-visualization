# 3D visualization of a Microscale Microbial Ecology Model

This repository contains scripts to produce a 3D visualization of a Microscale Microbial Ecology Model in Blender.


## Producing a Movie

The scripts need to be run in Blender. They have to be copied to Blender's **scripts** tab.

In the picture below you can see a general overview of the steps required to create a movie from a dataset. The dataset needs to be placed into the `data` folder. An example dataset can be found under `data/example`.

All scripts have to be run with the `DATA_LOCATION` environment variable set to the data folder location. From a bash shell you can simply run `DATA_LOCATION=/path/to/data/folder blender`

![image](https://github.com/meytin1337/3d-microbial-model-visualization/assets/15246633/cb76cee4-3f5c-477e-afaa-c168dcbf52a6)


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
