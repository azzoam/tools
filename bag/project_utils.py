import os
import os.path
import toml


def load_project(project_toml_file = "project.toml"):

    home_dir = os.path.expanduser("~")
    root_dir = "/"

    original_dir = os.getcwd()
    cwd = os.getcwd()

    running = (cwd != home_dir) and (cwd != root_dir)
    found = False
    while running:
        if os.path.isfile(project_toml_file):
            found = True
            break

        os.chdir("..")
        cwd = os.getcwd()
        running = (cwd != home_dir) and (cwd != root_dir)

    if found:
        toml_dict = toml.load(project_toml_file)
        os.chdir(original_dir)
        toml_dict["project_root"] = cwd
        return toml_dict
    else:
        return None
