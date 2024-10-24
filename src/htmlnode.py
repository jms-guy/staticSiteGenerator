class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
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
    

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
         if not self.value or self.value == "" or self.value == None:
              raise ValueError
         if not self.tag:
              return f"{self.value}"
         
         prop_string = self.props_to_html()
         return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"
         
