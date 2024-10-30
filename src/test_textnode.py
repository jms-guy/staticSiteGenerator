import unittest

from textnode import *
from split_nodes import *

class TestExtractMarkdownImages(unittest.TestCase):
    def test_basics(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extract_markdown_images(text))

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extract_markdown_links(text))

class TestSplitNodesFunction(unittest.TestCase):
    def test_basics(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ],
            new_nodes)
        
    def test_empty_segment(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ],
            new_nodes)
        
    def test_empty_end_segment(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            ],
            new_nodes)
        
    def test_multiple_bold(self):
        node = TextNode("This is text with a **bold block****bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ],
            new_nodes)
        
    def test_multiple_bold2(self):
        node = TextNode("This is **bold** text with a **bold block****bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ],
            new_nodes)
        
    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ],
            new_nodes)
        
    def test_italic(self):
        node = TextNode("This is text with a *italic block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ],
            new_nodes)
        
    def test_missing_syntax(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
            self.assertEqual(str(context.exception), "Invalid Markdown syntax")
        
    def test_missing_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node], "", TextType.CODE)
            self.assertEqual(str(context.exception), "No delimiter")
        
    def test_none_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node], None, TextType.CODE)
            self.assertEqual(str(context.exception), "No delimiter")

class TestConvertFunction(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        result = text_node_to_html_node(node)
        self.assertEqual("This is a text node", result.value)
        self.assertEqual("b", result.tag)

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        result = text_node_to_html_node(node)
        self.assertEqual("This is a text node", result.value)
        self.assertEqual("i", result.tag)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        result = text_node_to_html_node(node)
        self.assertEqual("This is a text node", result.value)

    def test_exception1(self):
        node = TextNode("This is a text node", 4)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_exception2(self):
        node = TextNode("This is a text node", "sdfkjhrg")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.google.com")
        result = text_node_to_html_node(node)
        self.assertEqual("This is a text node", result.value)
        self.assertEqual("a", result.tag)
        self.assertEqual({'href': 'www.google.com'}, result.props)

    def test_image(self):
        node = TextNode("This is image text", TextType.IMAGE, "www.google.com")
        result = text_node_to_html_node(node)
        self.assertEqual("", result.value)
        self.assertEqual("img", result.tag)
        self.assertEqual({'src': 'www.google.com', 'alt': 'This is image text'}, result.props)

    




class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_two(self):
        node = TextNode("A second test node", TextType.ITALIC, None)
        node2 = TextNode("A second test node", TextType.ITALIC, None)
        self.assertEqual(node, node2)

    def test_three(self):
        node = TextNode("It works!", TextType.TEXT, "www.wholesomeness.com")
        node2 = TextNode("It works!", TextType.TEXT, "www.wholesomeness.com")
        self.assertEqual(node, node2)

    def test_four(self):
        node = TextNode("Does this work?", TextType.ITALIC)
        node2 = TextNode("It hopefully won't", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_five(self):
        node = TextNode("It works!", TextType.CODE)
        node2 = TextNode("It works!", TextType.ITALIC)
        self.assertNotEqual(node, node2)  
    def test_six(self):
        node = TextNode("It works!", TextType.TEXT, "www.wholesomeness.com")
        node2 = TextNode("It works!", TextType.TEXT, "www.notwholesome.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a test", TextType.IMAGE, "www.url.com")
        self.assertEqual("TextNode(This is a test, TextType.IMAGE, www.url.com)",  repr(node))


if __name__ == "__main__":
    unittest.main()
