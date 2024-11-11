import unittest

from htmlnode import *


class TestParentNode(unittest.TestCase):
    def test_basics(self):
        node = ParentNode(
            [
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            )
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())

    def test_no_children(self):
        node = ParentNode([], "p")
        with self.assertRaises(ValueError) as context:
            node.to_html()
            self.assertEqual(str(context.exception), "No children")

    def test_none_children(self):
        node = ParentNode(None, "p")
        with self.assertRaises(ValueError) as context:
            node.to_html()
            self.assertEqual(str(context.exception), "No children")

    def test_no_tags(self):
        node = ParentNode([
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ])
        with self.assertRaises(ValueError) as context:
            node.to_html()
            self.assertEqual(str(context.exception), "No tag")

    def test_parent_children(self):
        node = ParentNode(
            [ParentNode(
            [
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            ),
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            )
        self.assertEqual("<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())

    def test_multiple_parent_children(self):
        node = ParentNode(
            [ParentNode(
            [
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            ),
            ParentNode(
            [
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            ),
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            )
        self.assertEqual("<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())

    def test_parent_children_parent(self):
        node = ParentNode(
            [ParentNode(
            [
            ParentNode(
            [
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            ),
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            ),
            LeafNode("Bold text", "b"),
            LeafNode("Normal text", None),
            LeafNode("italic text", "i"),
            LeafNode("Normal text", None),
            ],
            "p",
            )
        self.assertEqual("<p><p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())

class TestLeafNode(unittest.TestCase):
    def test_basics(self):
        node = LeafNode("This is value text", "p")
        self.assertEqual("<p>This is value text</p>", node.to_html())

    def test_no_value(self):
        node = LeafNode("", "p")
        with self.assertRaises(ValueError):
            node.to_html()
        
    def test_no_value2(self):
        node = LeafNode(None, "p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_tag(self):
        node = LeafNode("This is value text")
        self.assertEqual("This is value text", node.to_html())

    def test_props(self):
        node = LeafNode("This is value text", "a", {"href": "www.google.com"})
        self.assertEqual('<a href="www.google.com">This is value text</a>', node.to_html())

class TestHTMLNode(unittest.TestCase):
    def test_basics(self):
        node = HTMLNode("h1", "This is text value", children=None, props={"href": "www.google.com", "target": "_blank",})
        self.assertEqual("HTMLNode(h1, This is text value, [], {'href': 'www.google.com', 'target': '_blank'})", repr(node))

    def test_missing(self):
        node = HTMLNode("h1", "This is text value", props={"href": "www.google.com", "target": "_blank",})
        self.assertEqual("HTMLNode(h1, This is text value, [], {'href': 'www.google.com', 'target': '_blank'})", repr(node))

    def test_conversion(self):
        node = HTMLNode("h1", "This is text value", props={"href": "www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), " href=\"www.google.com\" target=\"_blank\"")

    def test_conversion_two(self):
        node = HTMLNode("h1", "This is text value", None, {"target": "_blank",})
        self.assertEqual(node.props_to_html(), " target=\"_blank\"")

    def test_conversion_three(self):
        node = HTMLNode("h1", "This is text value", props={"href": "www.google.com", "target": "_blank", "new": "who knows"})
        self.assertEqual(node.props_to_html(), " href=\"www.google.com\" new=\"who knows\" target=\"_blank\"")

    def test_conversion_four(self):
        node = HTMLNode("h1", "This is text value")
        self.assertEqual(node.props_to_html(), "") 

    def test_props_explicitly_none(self):
        node = HTMLNode("div", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_with_empty_values(self):
        node = HTMLNode("div", props={"data-test": "", "class": " "})
        self.assertEqual(node.props_to_html(), " class=\" \" data-test=\"\"")

    def test_props_with_special_chars(self):
        node = HTMLNode("div", props={"data-test": "hello&world", "class": "my-class!"})
        self.assertEqual(node.props_to_html(), " class=\"my-class!\" data-test=\"hello&amp;world\"")

    def test_props_with_quotes(self):
        node = HTMLNode("div", props={"data-msg": 'He said "hi"'})
        self.assertEqual(node.props_to_html(), " data-msg=\"He said &quot;hi&quot;\"")