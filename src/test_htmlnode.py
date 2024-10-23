import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_basics(self):
        node = HTMLNode("h1", "This is text value", children=None, props={"href": "www.google.com", "target": "_blank",})
        self.assertEqual("HTMLNode(h1, This is text value, None, {'href': 'www.google.com', 'target': '_blank'})", repr(node))

    def test_missing(self):
        node = HTMLNode("h1", "This is text value", props={"href": "www.google.com", "target": "_blank",})
        self.assertEqual("HTMLNode(h1, This is text value, None, {'href': 'www.google.com', 'target': '_blank'})", repr(node))

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