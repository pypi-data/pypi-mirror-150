#!/usr/bin/env python3

from html_string_tools.main.html_string_tools import remove_whitespace
from html import unescape
from typing import List
from re import findall

def get_blocks(text:str=None) -> List[str]:
    """
    Returns a list of string blocks from given HTML text.
    Broken up into normal text and HTML blocks.

    :param text: HTML text to split into blocks, defaults to None
    :type text: str, optional
    :return: List of string blocks from HTML text.
    :rtype: List[str]
    """
    try:
        # Get all HTML elements
        elements = findall("<[^<>]+>", text)
        # Separate out elements from text
        blocks = []
        left_text = text
        for element in elements:
            index = left_text.find(element)
            blocks.append(left_text[:index])
            blocks.append(element)
            left_text = left_text[index+len(element):]
        blocks.append(left_text)
        # Remove empty items from block list
        while True:
            try:
                index = blocks.index("")
                del blocks[index]
            except ValueError:
                break
        # Return blocks
        return blocks
    except TypeError:
        return []

def clean_element(html:str=None, remove_ends:str=False) -> str:
    """
    Cleans up HTML element.
    Removes whitespace and removes header and footer tags.

    :param html: HTML element, defaults to None
    :type html: str, optional
    :param remove_ends: Whether to remove header and footer tags, defaults to None
    :type remove_ends: bool, optional
    :return: Cleaned HTML element
    :rtype: str
    """
    # RETURNS EMPTY STRING IF GIVEN ELEMENT IS NONE
    if html is None:
        return ""
    # REMOVE NEW LINE AND CARRIAGE RETURN CHARACTERS
    text = html.replace("\n", "")
    text = text.replace("\r", "")
    # REMOVE WHITESPACE BETWEEN TAGS
    while "  <" in text:
        text = text.replace("  <", " <")
    while ">  " in text:
        text = text.replace(">  ", "> ")
    # REMOVE HEADER AND FOOTER, IF SPECIFIED
    if remove_ends:
        text = remove_whitespace(text)
        # REMOVE HEADER
        if len(text) > 0 and text[0] == "<":
            start = text.find(">")
            if not start == -1:
                text = text[start + 1:len(text)]
        # REMOVE FOOTER
        if len(text) > 0 and text[-1] == ">":
            end = text.rfind("<")
            if not end == -1:
                text = text[0:end]
    # REMOVE WHITESPACE FROM THE START AND END OF STRING
    text = remove_whitespace(text)
    return text

def remove_html_tags(text:str=None) -> str:
    """
    Removes HTML from given text, leaving only standard text.

    :param text: HTML text to remove tags from, defaults to None
    :type text: str, optional
    :return: HTML with the HTML tags removed
    :rtype: str
    """
    # Separate HTML into blocks
    blocks = get_blocks(text)
    # Remove HTML tags from blocks
    index = 0
    while index < len(blocks):
        if blocks[index][0] == "<":
            del blocks[index]
            continue
        index += 1
    # Combine remaining blocks into HTML string
    html = ""
    for i in range(0, len(blocks)):
        if i > 0:
            html = html + " "
        html = html + blocks[i]
    # Return HTML with tags removed
    return html

def create_html_tag(tag:str=None,
            attributes:List[List[str]]=None,
            text:str=None,
            pad_text:bool=True) -> str:
    """
    Creates an HTML tag with given parameters and contained text.

    :param tag: String for the tag itself (a, div, etc.), defaults to None
    :type tag: str, optional
    :param attributes: List of tag attribute pairs (Organized [attr, value]), defaults to None
    :type attributes: list[list[str]]
    :param text: Text to put inside the HTML tag, defaults to None
    :type text: str, optional
    :param pad_text: Whether to put internal text on a new line with tabs, defaults to True
    :type pad_text: bool, optional
    :return: HTML tag
    :rtype: str
    """
    # Return empty string if parameters are invalid
    if tag is None:
        return ""
    try:
        # Create the end of the HTML tag
        tag_end = ""
        if text is not None:
            tag_end = "</" + tag + ">"
        # Create the start of the HTML tag
        tag_start = "<" + tag
        # Add attributes to HTML tag
        if attributes is not None:
            for attribute in attributes:
                tag_start = tag_start + " " + attribute[0]\
                            +"=\"" + attribute[1] + "\""
        tag_start = tag_start + ">"
        # Add padding to the internal text of the tag if specified
        inner_text = text
        if inner_text is None:
            inner_text = ""
        if pad_text and text:
            inner_text = inner_text.replace("\n", "\n    ")
            inner_text = "\n    " + inner_text + "\n"
        # Create and return the full HTML tag
        tag = tag_start + inner_text + tag_end
        return tag
    except (IndexError, TypeError):
        # Return empty string if creating HTML tag fails
        return ""
