import re, os
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_nodes import *
from block_functions import *
from dir_to_dir import dir_to_dir


source_path = os.path.expanduser(r"~/workspace/github.com/jms-guy/staticSiteGenerator/static")
destination_path = os.path.expanduser(r"~/workspace/github.com/jms-guy/staticSiteGenerator/public")

def main():
    dir_to_dir(source_path, destination_path)


if __name__ == "__main__":
    main()
