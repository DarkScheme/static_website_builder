import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)

    def test_more_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("something else", TextType.BOLD)
        ja = node.__eq__(node2)
        nein = node.__eq__(node3)
        self.assertEqual(ja, True)
        self.assertNotEqual(nein, True)

    def test_repr(self):
        node = TextNode("abc", TextType.IMG, "https://")
        printed = node.__repr__()
        self.assertEqual("TextNode(abc, image, https://)", printed)
        self.assertNotEqual("abc, 123, https://", printed)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a BOLD node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMG, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )


if __name__ == "__main__":
    unittest.main()