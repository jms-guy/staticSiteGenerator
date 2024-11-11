from textnode import *
from htmlnode import *
from split_nodes import *

def markdown_to_html_node(markdown_document):
    blocks = markdown_to_blocks(markdown_document)
    html_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            result = block_to_heading(block)
        elif block_type == "code":
            result = block_to_code(block)
        elif block_type == "quote":
            result = block_to_quote(block)
        elif block_type == "unordered_list":
            result = block_to_unordered_list(block)
        elif block_type == "ordered_list":
            result = block_to_ordered_list(block)
        elif block_type == "paragraph":
            result = block_to_paragraph(block)
        html_blocks.append(result)
    return HTMLNode("div", None, html_blocks)
        

def block_to_heading(block):
    words = block.split()
    count = 0
    for char in words[0]:
        if char == "#":
            count +=1
    if count < 1 or count > 6:
        raise ValueError
    return HTMLNode(f"h{count}", None, text_to_children(block.lstrip("# ")))

def block_to_code(block):
    lines = block.split("\n")
    code_lines = lines[1:-1]
    code_block = TextNode(("\n".join(code_lines)), "text")
    code_node = HTMLNode("code", None, [code_block])
    return HTMLNode("pre", None, [code_node])

def block_to_quote(block):
   node = HTMLNode("blockquote", None, text_to_children(block.lstrip("> ")))
   return node

def block_to_unordered_list(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        children.append(HTMLNode("li", None, text_to_children(line.lstrip("* "))))
    return HTMLNode("ul", None, children)

def block_to_ordered_list(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        strippped_line = line.lstrip("1234567890. ")
        children.append(HTMLNode("li", None, text_to_children(strippped_line)))
    return HTMLNode("ol", None, children)

def block_to_paragraph(block):
    node = HTMLNode("p", None, text_to_children(block))
    return node


def text_to_children(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes

def markdown_to_blocks(document):
    blocks = document.split("\n\n")
    final_blocks = []

    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            final_blocks.append(stripped)
    return final_blocks 


def block_to_block_type(block):
    prefix = "######"
    if any(block.startswith(f"{prefix[:i]} ") for i in range(1, 7)):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    block_lines = block.split("\n")
    if all(line.startswith(">") for line in block_lines):
        return "quote"
    elif all((line.startswith("* ") or line.startswith("- ")) for line in block_lines):
        return "unordered_list"
    elif check_sequence(block_lines):
        return "ordered_list"
    else:
        return "paragraph"
    
### Function for checking for ordered lists in blocks
def check_sequence(lines):
    expected = 1
    for line in lines:
        if not line.startswith(f"{expected}. "):
            return False
        expected += 1
    return True
