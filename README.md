
# pNanoLocz <img src="https://github.com/Heath-AFM-Lab/pNanoLocz/assets/121131585/d7750a3c-f480-4c2e-b5fd-5317ca3dfa35" width="50">
Project to develop a Python version of NanoLocz Atomic Force Microscopy Analysis Platform 

This project is in the early stages of development.

# Instructions for activation

We are using a conda environment to run the appplication as it has prospects for future data science and machine learning functionality and good dependancy resolution. A script ideally will be developed to automatically set up the development environment, but for now the following should suffice.

Ananconda needs to be installed before running the application. You can find this on the [official Anaconda distribution page](https://www.anaconda.com/download). When running the installer, add anaconda to the PATH vaiables if on Windows

To initialise conda on the command line, run
`conda init`

To create the environment, run
`conda create --name pNanoLocz_env python=3.11`
This will create an environment on your machine that will store all the dependancies required by the program.

To activate the environment, run

On Windows:
`conda activate pNanoLocz_env`

On macOS/Linux:
`source activate pNanoLocz_env`

This will switch your PC to the development environment that will now contain the necessary dependancy files. Navigate to the folder containing the file `Requirements.txt`. We will now install these dependancies by running
`pip install -r Requirements.txt`

Once that is completed, we can run the program by running
`python main.py`

