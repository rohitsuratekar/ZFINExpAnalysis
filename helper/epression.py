"""
Rohit Suratekar
March 2019

Function to extract the expression data from ZFIN database
(https://zfin.org/downloads)
"""

from constants import *
from models.objects import *


def get_developmental_stages() -> dict:
    all_dev_stages = {}
    with open(FILE_STAGE) as f:
        for line in f:
            entries = line.strip().split("\t")
            if len(entries) == 5:  # Removes wrong entries
                if entries[0] != "Stage ID":  # Removes Header
                    d = DevelopmentalStage(entries)
                    all_dev_stages[d.stage_name] = d
    return all_dev_stages


def get_anatomy_items() -> dict:
    anatomy_items = {}
    with open(FILE_ANATOMY_ITEMS) as f:
        for line in f:
            if len(line.split("\t")) == 4:
                a = AnatomyItem(line)
                anatomy_items[a.id] = a
    # Additional item for missing entries
    missing = AnatomyItem("ZFA:0100000\tzebrafish\tanatomical entity\tNone\tNone")
    anatomy_items[missing.id] = missing
    return anatomy_items


def get_anatomy_relations() -> dict:
    relations = {}
    with open(FILE_ANATOMY_RELATIONSHIP) as f:
        for line in f:
            if len(line.split("\t")) == 3:
                r = AnatomyRelation(line.strip())
                relations[r.child] = r

    # Additional item for missing entries
    missing = AnatomyRelation("ZFA:0100000\tZFA:0100000\tis_a")
    relations[missing.child] = missing
    return relations


def get_expression_data() -> list:
    stages = get_developmental_stages()
    anatomy = get_anatomy_items()
    relations = get_anatomy_relations()
    data = []
    with open(FILE_EXPRESSION) as f:
        for line in f:
            entries = line.strip().split("\t")
            if len(entries) == 15:  # Removes wrong entries
                if entries[0] != "Gene ID":  # Removes Header
                    data.append(ExpressionEntry(entries, stages, anatomy, relations))

    return data


def test():
    get_expression_data()
