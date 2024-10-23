from textnode import TextType, TextNode
from htmlnode import HTMLNode

def main():
    node = HTMLNode("a", props={"href": "https://test.com?a=1&b=2"})
    result = node.props_to_html()
    print(result)



if __name__ == "__main__":
    main()
