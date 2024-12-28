Updating OpenABC torch objects

Create a VM 
- Create an Ubuntu 20.04 LTS machine
- 50 GB disk
- After
sudo apt update

Install needed packages
sudo apt install gcc
sudo apt install software-properties-common
3
sudo apt update
sudo apt install python3.9
sudo apt install python3-pip
sudo apt install python3.9-venv
sudo apt-get install python3.9-dev
—pip install pybind11>2.12

Clone repos
git clone https://github.com/CentralHubb/GNN-Synthesis.git

In the Download directory: 
- Create virtual environment 
python3.9 -m venv venv
source venv/bin/activate

- Install old torch and PyG
pip install torch==1.8.1
pip install torch-geometric==1.7.0

-Install torch extensions from source
pip install torch-scatter==2.0.8 -f https://data.pyg.org/whl/torch-1.8.1%2Bcu102.html
pip install torch-sparse==0.6.12 -f https://data.pyg.org/whl/torch-1.8.1%2Bcu102.html

-Downgrade numpy for use with old pytorch and PyG
pip uninstall numpy 
pip install numpy==1.22.4

-Install Google cloud
pip install google-cloud-storage

-In the Upload directory
python3.9 -m venv venv
pip install torch torch-geometric
pip install google-cloud-storage

-Update the databucket .json files for authentication

Run extract.py and transform.py in the download and upload directories at the same time

This will convert all .pt files created with PyG==1.7.0. Some files were saved with PyG==2.0.0. So they will error. 
Now, change to PyG 2.0.0

- Update PyG for other pt files
pip uninstall torch-geometric
pip install torch-geometric==2.0.0
python extract.py
