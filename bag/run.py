#!/usr/bin/env python3

import os
import os.path
import subprocess
import project_utils


def run(project_toml_file = "project.toml"):

    project_toml = project_utils.load_project(project_toml_file)

    if project_toml != None:
        if 'run' in project_toml:
            if 'program' in project_toml['run']:
                program = project_toml['run']['program']
                program = program.replace(
                        "${PH}", project_toml['project_root'])
                if os.path.isfile(program):
                    working_dir = os.getcwd()
                    args = []
                    if 'working_dir' in project_toml['run']:
                        working_dir = project_toml['run']['working_dir']
                        working_dir = working_dir.replace(
                                "${PH}", project_toml['project_root'])
                        if not os.path.isdir(working_dir):
                            working_dir = os.getcwd()
                    if 'args' in project_toml['run']:
                        args = project_toml['run']['args']
                        if type(args) is not list:
                            args = [args]
                    os.chdir(working_dir)
                    print("Working directory: {}".format(working_dir))
                    print("Args: {}".format(args))
                    args.insert(0, program)
                    subprocess.call(args)
                else:
                    print("Error: Program file {} not found.".format(
                        program))
            else:
                print("Error: No 'program' variable provided to [run] in {}"\
                        .format(os.path.join(
                            project_toml['project_root'], project_toml_file)))
        else:
            print("Error: No [run] config specified in {}".format(
                os.path.join(
                    project_toml['project_root'], project_toml_file)))
    else:
        print("Error: No project.toml fild found.  Exiting.")


if __name__ == "__main__":
    run()
