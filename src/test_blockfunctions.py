import unittest

from textnode import *
from split_nodes import *
from block_functions import *

class TestBlocktoBlockType(unittest.TestCase):

    def test_ordered_list(self):
        block = "1. Ordered\n2. List\n3. One"
        self.assertEqual("ordered_list", block_to_block_type(block))

    def test_ordered_list2(self):
        block = "1. Ordered\n2. List\n3. One"
        self.assertEqual("ordered_list", block_to_block_type(block))

    def test_heading1(self):
        block = "# Heading 1\n## Heading 2\n### Heading 3"
        self.assertEqual("heading", block_to_block_type(block))

    def test_heading2(self):
        block = "# Heading 1\n## Heading 2\n### Heading 3\n#### Heading 4\n##### Heading 5\n###### Heading 6"
        self.assertEqual("heading", block_to_block_type(block))

    def test_code(self):
        block = "```\nCode block\n```"
        self.assertEqual("code", block_to_block_type(block))

    def test_quote(self):
        block = ">Quote\n>Block"
        self.assertEqual("quote", block_to_block_type(block))
    
    def test_unordered_list1(self):
        block = "* Unordered\n* List\n- One"
        self.assertEqual("unordered_list", block_to_block_type(block))

    def test_unordered_list2(self):
        block = "- Unordered\n- List\n- Two"
        self.assertEqual("unordered_list", block_to_block_type(block))

class TestMarkdowntoBlocks(unittest.TestCase):
    
    def test_basics(self):
        doc = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"],
                         markdown_to_blocks(doc))
        
    def test_whitespace_removal(self):
        doc = "First line\n\n     Second     line     \n\n Third\n  and fourth\n line     "
        self.assertEqual(["First line", "Second     line", "Third\n  and fourth\n line"], markdown_to_blocks(doc))
    
    
    def test_empty_block(self):
        doc = "First line\n\nSecond line\n\n "
        self.assertEqual(["First line", "Second line"], markdown_to_blocks(doc))

    def test_empty_block2(self):
        doc = "First line\n\n \n\nSecond line\n\n "
        self.assertEqual(["First line", "Second line"], markdown_to_blocks(doc))

class TestCompiledSplitNodes(unittest.TestCase):
    def test_basics(self):
        test_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual([
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ], text_to_textnodes(test_text))
        
    def test_no_italic(self):
        test_text = "This is **text** with an `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual([
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ], text_to_textnodes(test_text))
        
    def test_no_image(self):
        test_text = "This is **text** with an *italic* word and a `code block` and a [link](https://boot.dev)"
        self.assertEqual([
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ], text_to_textnodes(test_text))
        
    def test_no_image_or_link(self):
        test_text = "This is **text** with an *italic* word and a `code block` and a "
        self.assertEqual([
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and a ", TextType.TEXT),
                    ], text_to_textnodes(test_text))