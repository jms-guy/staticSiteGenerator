import os, shutil


#This function will copy all contents from a source directory into a destination directory.

def dir_to_dir(source, destination):
    if os.path.exists(destination):
        for filename in os.listdir(destination):
            file_path = os.path.join(destination, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(destination)
    if os.path.exists(source):
        for filename in os.listdir(source):
            file_path = os.path.join(source, filename)
            if os.path.isfile(file_path):
                shutil.copy(file_path, destination)
            elif os.path.isdir(file_path):
                copied_dir = os.path.join(destination, filename)
                os.makedirs(copied_dir)
                dir_to_dir(file_path, copied_dir)
    else:
        raise OSError("Invalid source directory")
    


        
