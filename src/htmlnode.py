class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props

    def to_html(self):
            raise NotImplementedError
        
    def props_to_html(self):
            html_string = ""
            
            if self.props == None:
                return ""
            else:
                for prop in sorted(self.props):
                    modified_string = self.props[prop].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
                    html_string += f" {prop}=\"{modified_string}\""
            return html_string
        
    def __repr__(self):
            return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag or self.tag == "" or self.tag == None:
            raise ValueError("No tag")
        if not self.children or self.children == []:
            raise ValueError("No children")
        
        parent_value = ""
        for child in self.children:
            if hasattr(child, "to_html"):
                parent_value += child.to_html()
            else:
                parent_value += str(child)

        prop_string = self.props_to_html()
        return f"<{self.tag}{prop_string}>{parent_value}</{self.tag}>"

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag == "img":
            prop_string = self.props_to_html()
            return f"<{self.tag}{prop_string}/>" 
        if not self.value or self.value == "" or self.value == None:
            raise ValueError
        if not self.tag or self.tag == "" or self.tag == None:
            return f"{self.value}"
         
        prop_string = self.props_to_html()
        return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"
         
