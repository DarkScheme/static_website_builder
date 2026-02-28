from textnode import TextNode, TextType
from extracter import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        splitted = []
        spl = old_node.text.split(delimiter)
        splitted.extend(spl)

        if len(splitted) % 2 == 0:
            raise Exception("invalid Markdown text")
        else:
            i = 0
            while i < len(splitted):
                if splitted[i] == "":
                    i += 1
                    continue
                else:
                    if i % 2 == 0:
                        a = TextNode(splitted[i], TextType.TEXT)
                        result.extend([a])
                    else:
                        b = TextNode(splitted[i], text_type)
                        result.extend([b])
                i += 1
    return result



def split_nodes_image(old_nodes):
    return split_nodes_link_and_images(old_nodes, "image")

def split_nodes_link(old_nodes):
    return split_nodes_link_and_images(old_nodes, "link")

def split_nodes_link_and_images(old_nodes, decider):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        if decider == "image":
            list_of_tuples_stored = extract_markdown_images(old_node.text)
        elif decider == "link":
            list_of_tuples_stored = extract_markdown_links(old_node.text)
        else:
            raise Exception("wrong decider used")
        if list_of_tuples_stored == []: #no links/imgs in markdown
            result.append(old_node)
        else: #there are links/imgs
            remaining = old_node.text

            for tuple_stored in list_of_tuples_stored:
                if decider == "image":
                    delimiter = f'![{tuple_stored[0]}]({tuple_stored[1]})'
                elif decider == "link":
                    delimiter = f'[{tuple_stored[0]}]({tuple_stored[1]})'
                else:
                    raise Exception("wrong decider used")
                spl = remaining.split(delimiter, 1)
                if len(spl) != 2:
                    raise ValueError("invalid markdown, link section not closed")
                
                if spl[0] != "":
                    a = TextNode(spl[0], TextType.TEXT)
                    result.append(a)
                if decider == "image":
                    b = TextNode(tuple_stored[0], TextType.IMG, tuple_stored[1])
                elif decider == "link":
                    b = TextNode(tuple_stored[0], TextType.LINK, tuple_stored[1])
                else:
                    raise Exception("wrong decider used")
                result.append(b)
                remaining = spl[1]
            if remaining != "":
                c = TextNode(remaining, TextType.TEXT)
                result.append(c)
    return result   
   


def text_to_textnodes(text):
    temp_text_node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([temp_text_node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


