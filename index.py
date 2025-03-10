import os
import stat
import sys
import getpass
import configparser

# Set up INI
config = configparser.ConfigParser()
config.read("config.ini")
config_output_path = config.get("output_path", "path")
user_folder = getpass.getuser()
if config_output_path == "":
    config_output_path = f"C:/Users/{user_folder}/Desktop"
    config.set("output_path", "path", config_output_path)
    print(f"Output path has been defaulted to {config_output_path}. Change this in the ini to change where file maps are saved.")
    with open("config.ini", "w") as f:
        config.write(f)

is_path_defined = False

def main():
    global is_path_defined
    while not is_path_defined:
        define_path()

def define_path():
    global is_path_defined
    defined_path = input("Enter path to map: ")
    
    if os.path.exists(defined_path):
        print(os.path.abspath(defined_path), "exists")
        is_path_defined = True
        try:
            output_name = input("Enter file name to save as: ")
            output_path = config.get("output_path", "path") + f"/{output_name}.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                sys.stdout = f
                print_directory_tree(defined_path)
                sys.stdout = sys.__stdout__
                print("Directory tree saved to", output_path)
                re_run = input("Do you want to map another directory? (y/n): ")
                if re_run == "y":
                    is_path_defined = False
                    main()
                else:
                    print("Exiting...")
        except PermissionError:
            print("Permission denied: Unable to access some directories or files.")
    else:
        print("Not a path")

def print_directory_tree(path, prefix=""):
    try:
        if os.path.isdir(path):
            if not is_hidden(path):
                print(prefix + "📁 " + os.path.basename(path) + "/")
                prefix += "    "
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.exists(item_path):
                        print_directory_tree(item_path, prefix)
                    else:
                        print(prefix + "[Path Not Found]")
        else:
            print(prefix + "📄 " + os.path.basename(path))
    except PermissionError:
        print(prefix + "[Permission Denied]")
    except FileNotFoundError:
        print(prefix + "[File Not Found]")

def is_hidden(filepath):
    return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    
if __name__ == "__main__":
    main()