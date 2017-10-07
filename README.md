# CMakeProjectCreator
Quick python script to create boiler plate cmake project

usage: create_cmake_project.py [-h] [-y] [-lib] [-no_main]
                               project_name location author

Create Cmake project.

positional arguments:
  project_name  Name of the project
  location      Directory to create project
  author        Project Author

optional arguments:
  -h, --help    show this help message and exit
  -y            Run without asking for confirmation
  -lib          Makes a lib instead of a exe (no main.cpp is made)
  -no_main      Do not create a default main.cpp