import unittest

from textnode import *
from split_nodes import *
from block_functions import *

class TestBlocktoBlockType(unittest.TestCase):

    def test_ordered_list_with_inline_markdown(self):
        markdown = "1. Plain text\n2. Text with **bold** content\n3. Text with *italic* content"
        node = markdown_to_html_node(markdown)
    
        # Check root structure
        assert node.tag == "div"
        assert len(node.children) == 1  # Just one block - the ordered list
    
        # Get the ol node
        ol_node = node.children[0]
        assert ol_node.tag == "ol"
        assert len(ol_node.children) == 3  # Three list items
    
        # Check plain text item
        plain_item = ol_node.children[0]
        assert len(plain_item.children) == 1
        assert plain_item.children[0].tag == None
        assert plain_item.children[0].value == "Plain text"
    
        # Check bold item
        bold_item = ol_node.children[1]
        assert len(bold_item.children) == 3  # text, bold, text
        assert bold_item.children[1].tag == "b"
    
        # Check italic item
        italic_item = ol_node.children[2]
        assert len(italic_item.children) == 3  # text, italic, text
        assert italic_item.children[1].tag == "i"

    def test_markdown_multiple_blocks(self):
        text = "This is a paragraph\n\n```\nThis is a code block\n```\n\nThis is another paragraph"
        node = markdown_to_html_node(text)
    
        assert node.tag == "div"
        assert len(node.children) == 3
    
        # First paragraph
        assert node.children[0].tag == "p"
        assert node.children[0].children[0].value == "This is a paragraph"
    
        # Code block
        assert node.children[1].tag == "pre"
        assert node.children[1].children[0].tag == "code"
        assert node.children[1].children[0].children[0].text == "This is a code block"
    
        # Second paragraph
        assert node.children[2].tag == "p"
        assert node.children[2].children[0].value == "This is another paragraph"

    def test_unordered_list_with_inline_markdown(self):
        markdown = "* Plain text\n* Text with **bold** content\n* Text with *italic* content"
        node = markdown_to_html_node(markdown)
    
        # Check root structure
        assert node.tag == "div"
        assert len(node.children) == 1  # Just one block - the unordered list
    
        # Get the ul node
        ul_node = node.children[0]
        assert ul_node.tag == "ul"
        assert len(ul_node.children) == 3  # Three list items
    
        # Check plain text item
        plain_item = ul_node.children[0]
        assert len(plain_item.children) == 1
        assert plain_item.children[0].tag == None
        assert plain_item.children[0].value == "Plain text"
    
        # Check bold item
        bold_item = ul_node.children[1]
        assert len(bold_item.children) == 3  # text, bold, text
        assert bold_item.children[1].tag == "b"
    
        # Check italic item
        italic_item = ul_node.children[2]
        assert len(italic_item.children) == 3  # text, italic, text
        assert italic_item.children[1].tag == "i"

    def test_markdown_to_html_node(self):
        text = "This is a paragraph"
        node = markdown_to_html_node(text)

        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "p"
        assert node.children[0].children[0].value == "This is a paragraph"

    def test_markdown_to_heading(self):
        text = "# This is a heading"
        node = markdown_to_html_node(text)

        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "h1"
        assert node.children[0].children[0].value == "This is a heading"

    def test_markdown_to_heading2(self):
        text = "###### This is a heading"
        node = markdown_to_html_node(text)

        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "h6"
        assert node.children[0].children[0].value == "This is a heading"

    def test_markdown_to_quote(self):
        text = "> This is a quote"
        node = markdown_to_html_node(text)

        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "blockquote"
        assert node.children[0].children[0].value == "This is a quote"

    def test_markdown_to_code(self):
        text = "```\nThis is a code block\n```"
        node = markdown_to_html_node(text)

        assert node.tag == "div"
        assert len(node.children) == 1
        assert node.children[0].tag == "pre"
        assert node.children[0].children[0].tag == "code"
        assert node.children[0].children[0].children[0].text == "This is a code block"


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