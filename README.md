# Che293 Class Project
# Part 1: Molecular Dynamic Simulator using Python and Gromacs
Can be worked collaboratively with google colab
## Prerequisites
### If running from the terminal:
- Install miniconda

`pip install -y -c conda-forge gromacs`

`pip install -c conda-forge nglview "ipywidgets>=7,<8"`

Create a directory in your cwd with the same name as the protein's pdbID

Set environmental variables in shell if python is unable to locate your gmx path

- `export gmx_path='ABSOLUTE_PATH_TO_GMX'`

Upload the forcefield package you will be using for the simulations into your cwd

For this project, we use:
- Sirtuin-1 for our protein
- charmm36 for our forcefield
- 4ZZI for the pdbID

