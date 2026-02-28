from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from splitter import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            result.append(stripped)
    return result
                       

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block[0:3] == "```" and block[-3:] == "```" and len(lines) > 1:
        return BlockType.CODE
    elif block[0] == ">":
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block[0:2] == "- ":
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block[0:3] == "1. ":
        i = 0
        for line in lines:
            i += 1
            if not line.startswith(f'{i}. '):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def creater_heading(block):
    counter = block[0:6].count("#")
    tag = f"h{counter}"
    html_nodes = text_to_children(block[counter+1:])
    node = ParentNode(tag, html_nodes)
    return node

def creater_code(block):
    block = block[3:-3]
    block = block.lstrip("\n")
    #block = block.rstrip("\n")
    tnode = TextNode(block, TextType.CODE)
    node = text_node_to_html_node(tnode)
    return ParentNode("pre", [node])

def creater_quote(block):
    splitted = block.split("\n")
    text = ""
    for split in splitted:
        temp = split.lstrip(">")
        text += temp.lstrip(" ") + " "
    text = text.rstrip(" ")
    html_nodes = text_to_children(text)
    node = ParentNode("blockquote", html_nodes)
    return node

def creater_ul(block):
    splitted = block.split("\n")
    list_of_nodes = []
    for split in splitted:
        temp = split[2:]
        html_nodes_li = text_to_children(temp)
        nodes_li = ParentNode("li", html_nodes_li)
        list_of_nodes.append(nodes_li)
    node = ParentNode("ul", list_of_nodes)
    return node
   
def creater_ol(block):
    splitted = block.split("\n")
    list_of_nodes = []
    for split in splitted:
        i = split.index(".")
        temp = split[i+2:]
        html_nodes_li = text_to_children(temp)
        nodes_li = ParentNode("li", html_nodes_li)
        list_of_nodes.append(nodes_li)
    node = ParentNode("ol", list_of_nodes)
    return node

def creater_para(block):
    inline_block = block.replace("\n"," ")
    html_nodes = text_to_children(inline_block)
    node = ParentNode("p", html_nodes)
    return node

def markdown_to_html_node(markdown):
    splitted_blocks = markdown_to_blocks(markdown)

    list_of_nodes =[]
    for block in splitted_blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                new_HTML_node = creater_heading(block)
                list_of_nodes.append(new_HTML_node)
            case BlockType.CODE:
                new_HTML_node = creater_code(block)
                list_of_nodes.append(new_HTML_node)
            case BlockType.QUOTE:
                new_HTML_node = creater_quote(block)
                list_of_nodes.append(new_HTML_node)
            case BlockType.UNORDERED_LIST:
                new_HTML_node = creater_ul(block)
                list_of_nodes.append(new_HTML_node)
            case BlockType.ORDERED_LIST:
                new_HTML_node = creater_ol(block)
                list_of_nodes.append(new_HTML_node)
            case BlockType.PARAGRAPH:
                new_HTML_node = creater_para(block)
                list_of_nodes.append(new_HTML_node)
            case _:
                raise Exception("not a valid BlockType")
    
    node = ParentNode("div", list_of_nodes)
    return node
        










