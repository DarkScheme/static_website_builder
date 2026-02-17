import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    
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








if __name__ == "__main__":
    unittest.main()