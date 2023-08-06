#!/usr/bin/env python3

from html_string_tools.main.html_string_tools import remove_whitespace as rw
from html_string_tools.main.html_string_tools import replace_reserved_characters as rrc
from re import sub as re_sub
from typing import List

def clean_list(lst:List[str]=None, remove_whitespace:bool=True) -> List[str]:
    """
    Removes all duplicate, None, and blank entries from a String array.

    :param lst: Given string list
    :type lst: list[str], optional
    :param remove_whitespace: Whether to remove whitespace from list entries, defaults to True
    :type remove_whitespace: bool, optional
    :return: List without duplicate or None entries
    :rtype: list[str]
    """
    try:
        # Remove entries with None value
        out = lst
        while True:
            try:
                index = out.index(None)
                del out[index]
            except ValueError:
                break
        # Remove whitespace if specified
        if remove_whitespace:
            size = len(out)
            for i in range(0, size):
                out[i] = rw(out[i])
        # Remove entries with blank value
        while True:
            try:
                index = out.index("")
                del out[index]
            except ValueError:
                break
        # Remove duplicate entries
        out = list(dict.fromkeys(out))
        # Return modified list
        return out
    except AttributeError:
        return []

def list_to_string(lst:List[str], indent:int=0) -> str:
    """
    Converts list[str] into a string with items separated by commas.

    :param lst: List[str] to convert to string
    :type lst: list[str], required
    :param indent: Number of spaces to add after separating commas, defaults to 0
    :type indent: int, optional
    :return: String with original items separated by commas
    :rtype: str
    """
    try:
        # Add commas between list items
        list_string = ""
        for item in lst:
            list_string = list_string + rrc(item).replace(",", "&#44;") + ","
        # Add indents
        ind_string = ","
        for i in range(0, indent):
            ind_string = f"{ind_string} "
        list_string = list_string.replace(",", ind_string)
        # Remove the trailing comma
        true_indent = indent
        if true_indent < 0: true_indent = 0
        list_string = re_sub(",[ ]{" + str(true_indent) + "}$", "", list_string)
        # Return the finished string
        return list_string
    except TypeError: return ""
