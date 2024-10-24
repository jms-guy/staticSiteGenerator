from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode

def main():
    node = LeafNode("value", "a", {"href": "https://test.com?a=1&b=2"})
    print(node.to_html())



if __name__ == "__main__":
    main()
