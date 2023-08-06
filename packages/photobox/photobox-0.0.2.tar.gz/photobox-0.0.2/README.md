++========================
# PhotoBox v0.0.2
==========================
#### *Author:*    Ioannis Kalfas
#### *Contact:*   kalfasyan@gmail.com , ioannis.kalfas@kuleuven.be
#### *Role:*      PhD Researcher
#### *Division:*  MeBioS, KU Leuven
--------
## Features

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
--------
### Installation

1. First install `pcmanfm` file manager by running this in your terminal:   
`sudo apt-get update -y`  
`sudo apt-get install -y pcmanfm`  

2. Clone the `conda` environment from the file `conda_environment.yml` by running:  
`conda env create -f conda_environment.yml`

3. Download the extra files from [here](https://kuleuven-my.sharepoint.com/:f:/g/personal/ioannis_kalfas_kuleuven_be/EtfN74iqV5NJspAMBYX4b_UB3ynlQXdfRn7OC21v9T4EVA?e=LXv7HB) and paste them in the photobox folder (same dir as `photobox_app.py`)

4. Activate the `pbox` environment (`conda activate pbox`) and then run:  
   `python photobox_app.py`
  
  
### DISCLAIMER
--------
All data in this repo belong to KU Leuven.