import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode



class TestHTMLNode(unittest.TestCase):
    
    #####################################
    ### Below the tests for HTML Node ###
    #####################################

    def test_print(self):
        prop = {
            "key1": "value1",
            "key2": "value2",
        }
        node = HTMLNode("tag", "value")
        node2 = HTMLNode("tag2", None, [node])
        node3 = HTMLNode("tag3", "value3", None, prop)
        node_p = node.__repr__()
        node2_p = node2.__repr__()
        node3_p = node3.__repr__()
        #self.assertEqual("tag is: tag\nvalue is: value\nhas 0 children\nand this is the dict:\n", node_p)
        #self.assertEqual("tag is: tag2\nvalue is: None\nhas 1 children\nand this is the dict:\n", node2_p)
        #self.assertEqual('tag is: tag3\nvalue is: value3\nhas 0 children\nand this is the dict:\n key1="value1" key2="value2"', node3_p)
        self.assertEqual(node_p, "HTMLNode(tag, value, children: None, None)")
        self.assertEqual(node2_p, "HTMLNode(tag2, None, children: [HTMLNode(tag, value, children: None, None)], None)")
        self.assertEqual(node3_p, "HTMLNode(tag3, value3, children: None, {'key1': 'value1', 'key2': 'value2'})")
        
        child_value = node2.children[0].value
        self.assertEqual("value", child_value)
        self.assertEqual(node, node2.children[0])

    def test_props_to_html(self):
        prop = {
            "key1": "value1",
            "key2": "value2",
        }
        node = HTMLNode("tag3", "value3",None, prop)
        p_t_h = node.props_to_html()
        self.assertEqual(' key1="value1" key2="value2"', p_t_h)

    #####################################
    ### Below the tests for Leaf Node ###
    #####################################

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

        node3 = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node3.to_html()

        node4 = LeafNode(None, "that is only some text")
        self.assertEqual("that is only some text", node4.to_html())


    def test_leaf_repr(self):
        node = LeafNode("tag", "value", {"key": "value"})
        self.assertEqual("LeafNode(tag, value, {'key': 'value'})", node.__repr__())

        easy = LeafNode("tag", "value")
        self.assertEqual("LeafNode(tag, value, None)", easy.__repr__())

    #######################################
    ### Below the tests for Parent Node ###
    #######################################

    def test_parent_to_html(self):
        node = HTMLNode("tag", "value")
        nodeL = LeafNode("p", "Hello, world!")
        nodeP = ParentNode("ul", [nodeL])
        self.assertEqual(nodeP.to_html(), "<ul><p>Hello, world!</p></ul>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("p", "2nd child")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><p>2nd child</p></div>")

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "Object does NOT have children")

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "Object does NOT have a tag")

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


    






if __name__ == "__main__":
    unittest.main()