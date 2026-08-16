import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_noteq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "cool")
        node2 = TextNode("This is a text node", TextType.BOLD, "now")

        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "cool")
        node2 = TextNode("This is a text node", TextType.BOLD, "cool")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text nodes", TextType.BOLD, "cool")
        node2 = TextNode("This is a text node", TextType.BOLD, "now")

        self.assertNotEqual(node, node2)

    def test_not_eq_type_text_url(self):
        node = TextNode("This is a text nodes", TextType.PLAIN, "cool")
        node2 = TextNode("This is a text node", TextType.BOLD, "cool")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertNotEqual(html_node.value, "This is a text")

if __name__ == "__main__":
    unittest.main()
