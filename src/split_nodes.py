from textnode import *
from htmlnode import *
import re

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    step_one = split_nodes_image(nodes)
    step_two = split_nodes_link(step_one)
    step_three = split_nodes_delimiter(step_two, "**", TextType.BOLD)
    step_four = split_nodes_delimiter(step_three, "*", TextType.ITALIC)
    result = split_nodes_delimiter(step_four, "`", TextType.CODE)

    return result

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
                    raise Exception("Invalid markdown syntax")
                for index, segment in enumerate(split_nodes):
                    if segment != "":
                        if index % 2 == 0:
                            new_nodes.append(TextNode(segment, TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(segment, text_type))
            else:
                new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for original_node in old_nodes:
        original_text = original_node.text
        matches = extract_markdown_images(original_text)
        if matches == None:
            new_nodes.append(original_node)
            continue
        for image_alt, image_url in matches:
            match_string = f"![{image_alt}]({image_url})"
            text_parts = original_text.split(match_string, 1)
            if text_parts[0] != "":
                new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = text_parts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))      

        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for original_node in old_nodes:
        if original_node.text_type != TextType.TEXT:
            new_nodes.append(original_node)
            continue
        original_text = original_node.text
        matches = extract_markdown_links(original_text)
        if matches == None:
            new_nodes.append(original_node)
            return new_nodes
        for link_text, link_url in matches:
            match_string = f"[{link_text}]({link_url})"
            text_parts = original_text.split(match_string, 1)
            if text_parts[0] != "":
                new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = text_parts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))      

        
    return new_nodes

                        

def extract_markdown_images(text):
    extracted_strs = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)     
    return extracted_strs



def extract_markdown_links(text):   
    extracted_strs = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_strs
                

