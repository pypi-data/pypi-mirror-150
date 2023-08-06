===============================
# PhotoBox v0.0.1
===============================

### Features
--------
* Handles imaging sessions
* Capture a sticky plate image
* Spatial (applied) and color calibration (available).
* Cropping.
* Object detection on the captured image.
* Model inference on detected objects/insects.
* Validation procedure for entomology experts.
* Exporting all results in csv files.
* Creating plots with insect counts.
* Works on both a Raspberry Pi and any PC.

## DISCLAIMER
--------
All data in this repo belong to KU Leuven.

### Installation
1. First install `pcmanfm` file manager.
`sudo apt-get update -y`
`sudo apt-get install -y pcmanfm`

2. Clone the `conda` environment from the file `conda_environment.yml`

3. Run `python photobox_app.py`