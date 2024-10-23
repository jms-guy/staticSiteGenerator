import unittest

from textnode import TextNode, TextType


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
        node = TextNode("It works!", TextType.NORMAL, "www.wholesomeness.com")
        node2 = TextNode("It works!", TextType.NORMAL, "www.wholesomeness.com")
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
        node = TextNode("It works!", TextType.NORMAL, "www.wholesomeness.com")
        node2 = TextNode("It works!", TextType.NORMAL, "www.notwholesome.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a test", TextType.IMAGES, "www.url.com")
        self.assertEqual("TextNode(This is a test, images, www.url.com)",  repr(node))


if __name__ == "__main__":
    unittest.main()
