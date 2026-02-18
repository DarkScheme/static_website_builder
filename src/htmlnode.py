



class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              #string
        self.value = value          #string
        self.children = children    #list of htmlnode ogjects
        self.props = props          #dict of key value pairs representing html attributes. e.g. {"href": "https...."}
        

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            glue = ""
            for k, v in self.props.items():
                glue += f' {k}="{v}"'
            return glue
        
    def __repr__(self):
        # if self.children is None:
        #     children_number = 0
        # else:
        #     children_number = len(self.children)
        #return f"tag is: {self.tag}\nvalue is: {self.value}\nhas {children_number} children\nand this is the dict:\n{self.props_to_html()}"
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        if self.tag is None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Object does NOT have a tag")
        if self.children is None or self.children == []:
            raise ValueError("Object does NOT have children")
        else:
            message = ""
            for child in self.children:
                message += child.to_html()
            return "<" + self.tag + ">" + message + "</" + self.tag + ">"
        








