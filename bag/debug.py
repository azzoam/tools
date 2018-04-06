#!/usr/bin/env python3

import os
import os.path
import subprocess
import project_utils


def debug(project_toml_file = "project.toml"):

    project_toml = project_utils.load_project(project_toml_file)

    if project_toml != None:
        if 'debug' in project_toml:
            if 'program' in project_toml['debug']:
                program = project_toml['debug']['program']
                program = program.replace(
                        "${PH}", project_toml['project_root'])
                if os.path.isfile(program):
                    working_dir = os.getcwd()
                    args = []
                    if 'working_dir' in project_toml['debug']:
                        working_dir = project_toml['debug']['working_dir']
                        working_dir = working_dir.replace(
                                "${PH}", project_toml['project_root'])
                        if not os.path.isdir(working_dir):
                            working_dir = os.getcwd()
                    if 'args' in project_toml['debug']:
                        args = project_toml['debug']['args']
                        if type(args) is not list:
                            args = [args]
                    os.chdir(working_dir)
                    if 'debugger' in project_toml['debug']:
                        if project_toml['debug']['debugger'] == 'gdb':
                            debugger = 'gdb'
                        elif project_toml['debug']['debugger'] == 'lldb':
                            debugger = 'lldb'
                        else:
                            debugger = 'gdb'
                    else:
                        debugger = 'gdb'
                    print("Working directory: {}".format(working_dir))
                    print("Args: {}".format(args))
                    args.insert(0, debugger)
                    args.append(program)
                    subprocess.call(args)
                else:
                    print("Error: Program file {} not found.".format(
                        program))
            else:
                print("Error: No 'program' variable provided to [debug] in {}"\
                        .format(os.path.join(
                            project_toml['project_root'], project_toml_file)))
        else:
            print("Error: No [debug] config specified in {}".format(
                os.path.join(
                    project_toml['project_root'], project_toml_file)))
    else:
        print("Error: No project.toml fild found.  Exiting.")


if __name__ == "__main__":
    debug()
