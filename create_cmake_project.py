import argparse
import sys
import os, errno
import time

def build_main_cpp(author):
	return """/****************************
*
* Some description
*
* Author: """+author+"""
* Created: """ + time.strftime("%c")+"""
****************************/

#include <iostream>\n
int main(int argc, char* argv[]) {
	return 0;
}
		"""
	

# Don't mess with the formatting
def build_base_cmake_lists(project_name):
	return """cmake_minimum_required(VERSION 2.8.7 FATAL_ERROR)

project("""+ project_name +""")

set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/../bin)

# Find needed libraries

add_subdirectory(src)
"""

# Don't mess with the formatting
def build_src_cmake_lists(project_name, is_exe = True):
	include_str =  """include_directories(
	${PROJECT_SOURCE_DIR}/src
)
	
file( GLOB SRC 
	#INCLUDE
	${PROJECT_SOURCE_DIR}/src/*.h

	#SOURCE
	${PROJECT_SOURCE_DIR}/src/*.cpp
)

"""

	if is_exe:
		build_str = "add_executable("+project_name
	else:
		build_str = "add_library("+project_name
		
	build_str = build_str + "\n\t${SRC}\n)"
	return include_str + build_str
 
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def main():
	parser = argparse.ArgumentParser(description='Create Cmake project.')
	parser.add_argument('project_name', metavar='project_name', 
		help='Name of the project')
	parser.add_argument('location', metavar='location', 
		help='Directory to create project')
	parser.add_argument('author', metavar='author', 
		help='Project Author')
	parser.add_argument('-y', dest='y', action='store_true',
		help='Run without asking for confirmation')
	parser.add_argument('-lib', dest='lib', action='store_true',
		help='Makes a lib instead of a exe (no main.cpp is made)')
	parser.add_argument('-no_main', dest='lib', action='store_true',
		help='Do not create a default main.cpp')
	args = parser.parse_args()
	
	project_name = args.project_name
	location = args.location
	
	if not args.y:
		if not query_yes_no("Create Project: " + project_name + " in directory: " + location):
			exit()
	
	# Create the project folder structure
	if not os.path.exists(location):
		os.makedirs(location)
		os.makedirs(location + os.sep + "src")
		os.makedirs(location + os.sep + "bin")
		os.makedirs(location + os.sep + "docs")
		os.makedirs(location + os.sep + "cmake")
	else:
		print(location + " already exists. Exiting")
		exit()
	
	# Create base cmakelists
	file = open(location + os.sep + "CMakeLists.txt",'w')
	file.write(build_base_cmake_lists(project_name))
	file.close()
	
	# Create src cmakelists
	file = open(location + os.sep + "src" + os.sep + "CMakeLists.txt",'w')
	file.write(build_src_cmake_lists(project_name, not args.lib))
	file.close()
	
	# Create main
	if not args.lib and not args.no_main:
		file = open(location + os.sep + "src" + os.sep + "main.cpp",'w')
		file.write(build_main_cpp(args.author))
		file.close()

if __name__ == "__main__":
    main()