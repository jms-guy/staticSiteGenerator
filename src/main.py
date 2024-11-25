import re, os, shutil
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_nodes import *
from block_functions import *
from dir_to_dir import *


source_path = os.path.join("static")
destination_path = os.path.join("public")

def main():
    dir_to_dir(source_path, destination_path)
    generate_page('content/index.md', 'template.html', 'public/index.html')


if __name__ == "__main__":
    main()
