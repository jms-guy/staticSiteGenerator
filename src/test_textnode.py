import unittest

from textnode import *

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
