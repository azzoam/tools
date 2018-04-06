#!/usr/bin/env python3

import os
import os.path
import subprocess
import sys
import project_utils


def build(project_toml_file = "project.toml"):

    project_toml = project_utils.load_project(project_toml_file)

    if project_toml != None:
        if 'build' in project_toml:
            if 'script' in project_toml['build']:
                script_dir = project_toml['build']['script']
                script_dir = script_dir.replace(
                        "${PH}", project_toml['project_root'])
                if os.path.isfile(script_dir):
                    os.chdir(os.path.dirname(script_dir))
                    subprocess.call([script_dir])
                else:
                    print("Error: Build script {} not found.".format(
                        script_dir))
            else:
                print(
                "Error: No 'script' variable provided to [build] in {}".format(
                    os.path.join(
                        project_toml['project_root'], project_toml_file)))
        else:
            print("Error: No [build] config specified in {}".format(
                os.path.join(
                    project_toml['project_root'], project_toml_file)))
    else:
        print("Error: No project.toml file found.  Exiting.")



if __name__ == "__main__":
    build()
