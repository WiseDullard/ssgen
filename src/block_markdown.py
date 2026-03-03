from enum import Enum

from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    line = block.split("\n")[0]
    if line.startswith("#"):     
        i = 0
        while i < len(line) and line[i] == "#":
            i += 1
        if 1 <= i <= 6 and i < len(line) and line[i] == " ":
            return BlockType.HEADING
            
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    is_quote = True
    for line in lines:
        if not (line.startswith(">") or line.startswith("> ")):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    lines = block.split("\n")
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    
    lines = block.split("\n")
    is_ordered = True
    for index, line in enumerate(lines):
        expected_prefix = f"{index + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children.append(heading_helper(block))
        elif block_type == BlockType.CODE:
            children.append(code_helper(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_helper(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_helper(block))
        elif block_type == BlockType.QUOTE:
            children.append(quotes_helper(block))
        else:
            children.append(paragraph_helper(block))
    return ParentNode("div", children)
            
def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = []
    for tn in textnodes:
        children.append(text_node_to_html_node(tn))
    return children

def heading_helper(block):
    hashes, text = block.split(" ", maxsplit=1)
    level = len(hashes)
    tag = f"h{level}"
    children = text_to_children(text)
    return ParentNode(f"{tag}", children)

def code_helper(block):
    block = block.strip()
    lines = block.split("\n")
    inner_lines = lines[1:-1]
    code_text = "\n".join(inner_lines).rstrip()
    code_node = LeafNode("code", code_text)
    pre_node = ParentNode("pre", [code_node])
    return pre_node

def ordered_list_helper(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        first_space = line.find(" ")
        item_text = line[first_space + 1 :]
        children = text_to_children(item_text)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    return ParentNode("ol", li_nodes)

def unordered_list_helper(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        marker = line[0]
        if marker not in "-*":
            continue
        item_text = line[1:].lstrip()
        children = text_to_children(item_text)
        li_node = ParentNode("li", children)
        li_nodes.append(li_node)
    return ParentNode("ul", li_nodes)

def quotes_helper(block):
    lines = block.split("\n")
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not line.startswith(">"):
            continue
        line = line[1:].lstrip()
        clean_lines.append(line)
    item_text = " ".join(clean_lines)
    children = text_to_children(item_text)
    return ParentNode("blockquote", children)

def paragraph_helper(block):
    clean_text = block.replace("\n", " ")
    children = text_to_children(clean_text)
    return ParentNode("p", children)