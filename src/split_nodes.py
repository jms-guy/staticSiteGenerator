from textnode import *
from htmlnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if delimiter == "" or delimiter == None:
                raise Exception("No delimiter")
            if delimiter in node.text:
                split_nodes = node.text.split(f"{delimiter}")
                if len(split_nodes) % 2 == 0:
                    raise Exception("Invalid Markdown syntax")
                for index, segment in enumerate(split_nodes):
                    if segment != "":
                        if index % 2 == 0:
                            new_nodes.append(TextNode(segment, TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(segment, text_type))
            else:
                new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes
                        

def extract_markdown_images(text):
    extracted_strs = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)     
    return extracted_strs



def extract_markdown_links(text):   
    extracted_strs = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_strs
                

