from textnode import TextNode, TextType

def main():
    new_Node = TextNode("this is some anchor", TextType.LINK_TEXT, "https://www.boot.dev")
    print(new_Node)

main()