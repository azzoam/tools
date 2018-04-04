#!/usr/bin/env python3

import os
import os.path
import subprocess

def build(project_head_file = ".projecthead", build_file = "build.sh"):

    home_dir = os.path.expanduser("~")
    root_dir = "/"

    cwd = os.getcwd()
    running = (cwd != home_dir) and (cwd != root_dir)
    found = False
    pf_exists = False
    while running:
        if os.path.isfile(project_head_file):
            if os.path.isfile(build_file):
                found = True
                break
            else:
                pf_exists = True
                break

        os.chdir("..")
        cwd = os.getcwd()
        running = (cwd != home_dir) and (cwd != root_dir)

    if found:
        subprocess.call(['./' + build_file])
    elif pf_exists:
        print("No build.sh file found at project head.  Exiting.")
    else:
        print("No project head file found.  Exiting.")




if __name__ == "__main__":
    build()
