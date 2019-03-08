"""
Rohit Suratekar
March 2019

All basic Analysis Functions
"""

from helper.epression import get_expression_data


def get_available_entries(entry: str) -> list:
    entries = []
    for d in get_expression_data():
        if d.is_there(entry):
            entries.append(d)
    return entries


def get_expression_pattern_in(gene: str, parent_structure: str) -> list:
    entries = []
    for e in get_available_entries(gene):
        if parent_structure is not None:
            if parent_structure in e.super_structure.name:
                entries.append(e)
        else:
            entries.append(e)
    return entries


def run():
    print(len(get_expression_pattern_in("gata6", "")))
