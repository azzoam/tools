#!/usr/bin/env python3

import sys
import os.path
import os
import shutil
import stat

build_sh = \
"""#!/bin/bash
start=$(date +%s.%N)

PROGRAM_NAME="${project_name}"
COMPILER_FLAGS="-g -Wall -Werror"
DEFINES=""
LINKER_FLAGS=""

mkdir -p target
pushd target > /dev/null

echo "Compiling..."
g++ $COMPILER_FLAGS $DEFINES ../src/main.cpp -o $PROGRAM_NAME $LINKER_FLAGS 

popd > /dev/null

end=$(date +%s.%N)
runtime=$(python -c "print(round(${end} - ${start}, 3))")
echo "Compiled in $runtime seconds"
"""

toml_file = \
"""# Project TOML file
# NOTE: keep at root of project directory tree

[description]
name = "${project_name}"
authors = ["Alex Azzo <azzoa@vcu.edu>"]
version = "0.1"

[build]
script = "${PH}/build.sh"

[run]
program = "${PH}/target/${project_name}"
working_dir = "${PH}/data"
args = []

[debug]
debugger = "gdb"
program = "${PH}/target/${project_name}"
working_dir = "${PH}/data"
args = ["-q"]
"""

main_prog = \
"""#include <stdio.h>


int main(int argc, char **argv) {

    printf("It worked!\\n");
    return 0;
}
"""

def new(project_name):
    os.mkdir(project_name)
    os.chdir(project_name)
    os.mkdir('src')
    os.mkdir('data')
    os.mkdir('target')
    project_toml = toml_file.replace("${project_name}", project_name)
    build_script = build_sh.replace("${project_name}", project_name)
    with open('project.toml', 'w') as fh:
        fh.write(project_toml)
    with open('build.sh', 'w') as fh:
        fh.write(build_script)
    os.chmod('build.sh', 
            stat.S_IRWXU | stat.S_IRGRP | \
            stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    os.chdir('src')
    with open('main.cpp', 'w') as fh:
        fh.write(main_prog)


if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print("Error: Invalid arguments")
        print("Example usage:  'new project_name'")
    else:
        project_name = sys.argv[1]
        if os.path.exists(project_name):
            print("Error: {} already exists.  Aborting.".format(project_name))
        else:
            new(project_name)
