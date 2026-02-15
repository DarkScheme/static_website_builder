import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()