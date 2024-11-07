from textnode import *
from htmlnode import *
from split_nodes import *

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