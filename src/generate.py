import os, shutil
from block_functions import *


# Function to generate pages recursively

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_entries = os.listdir(dir_path_content)
    for filename in content_entries:
        file_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(file_path) and file_path.endswith(".md"):
            copied_path = os.path.join(dest_dir_path, filename).replace(".md", ".html")
            generate_page(file_path, template_path, copied_path)
        elif os.path.isdir(file_path):
            copied_dir = os.path.join(dest_dir_path, filename)
            os.makedirs(copied_dir, exist_ok=True)
            generate_pages_recursive(file_path, template_path, copied_dir)

#Function to generate a webpage of content

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path, "r") as file_handle:
            from_contents = file_handle.read()
    except FileNotFoundError:
        raise OSError("Invalid 'from' path")
    content_title = extract_title(from_contents)
    content_nodes = markdown_to_html_node(from_contents)
    content_html = content_nodes.to_html()

    try:
        with open(template_path, "r") as file_handle:
            template_content = file_handle.read()
        template_content = template_content.replace("{{ Title }}", content_title).replace("{{ Content }}", content_html)
    except FileNotFoundError:
        raise OSError("Invalid 'template' path")

    directory = os.path.dirname(dest_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as html_page:
        html_page.write(template_content)


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
    


        
