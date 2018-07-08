"""
Rohit Suratekar
July 2018

Basic analysis of zebrafish expression database present in ZFIN (
https://zfin.org)

All downloaded files are kept in "/database" folder
1. Expression data
2. Ontology data
3. Anatomy items
4. Anatomy data
"""

from collections import Counter

import matplotlib.pylab as plt
import numpy as np

from models import DataObject, get_parent_structure

FILENAME = "database\wildtype-expression_fish_2018.07.05.txt"


def get_data() -> list:
    all_obs = []
    with open(FILENAME) as f:
        for line in f:
            if len(line.split("\t")) == 14:
                all_obs.append(DataObject(line))

    return all_obs


def check_hist():
    c = Counter()
    for o in get_data():
        ob = o  # type: DataObject
        c.update({ob.super_structure.name})

    values = []
    labels = []

    for i in c.most_common(25):
        values.append(i[1])
        labels.append(i[0])

    figure = plt.figure()
    ax = figure.add_subplot(111)
    ind = np.arange(len(labels))
    width = 0.35
    ax.bar(ind, values, width, color="#e4adea")
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.xaxis.set_tick_params(rotation=90)
    plt.show()


def localization(gene, with_parent=False):
    no_of_genes = 25
    c = Counter()
    for o in get_data():
        ob = o  # type: DataObject
        if ob.gene_symbol == gene and with_parent:
            c.update({ob.parent_structure.name})

        if ob.gene_symbol == gene and not with_parent:
            c.update({ob.super_structure.name})

    values = []
    labels = []

    for i in c.most_common(no_of_genes):
        values.append(i[1])
        labels.append(i[0])

    figure = plt.figure()
    ax = figure.add_subplot(111)
    ind = np.arange(len(labels))
    width = 0.35
    ax.bar(ind, values, width, color="#e4adea")
    ax.set_ylabel(
        "number of reports in literature\n(6 July 2018, ZFIN database)")
    ax.set_xlabel("Structure")
    ax.set_title("top %d locations expressing $\\bf{%s}$" % (no_of_genes,
                                                             gene))
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.xaxis.set_tick_params(rotation=90)
    plt.show()


def genes_in_organ(organ):
    no_of_genes = 25
    c = Counter()
    for o in get_data():
        ob = o  # type: DataObject
        if ob.super_structure.name == organ:
            c.update({ob.gene_symbol})

    values = []
    labels = []

    for i in c.most_common(no_of_genes):
        values.append(i[1])
        labels.append(i[0])

    figure = plt.figure()
    ax = figure.add_subplot(111)
    ind = np.arange(len(labels))
    width = 0.35
    ax.bar(ind, values, width, color="#e4adea")
    ax.set_ylabel(
        "number of reports in literature\n(6 July 2018, ZFIN database)")
    ax.set_xlabel("gene symbol")
    ax.set_title("top %d genes expressing in $\\bf{%s}$" % (no_of_genes, organ))
    ax.set_xticks(ind)
    ax.set_xticklabels(labels)
    ax.xaxis.set_tick_params(rotation=90)
    plt.show()


def expression_profile(gene_name, organ=None, with_parent=False):
    start_stage = Counter()
    start_index = Counter()
    end_stage = Counter()
    end_index = Counter()
    for o in get_data():
        ob = o  # type: DataObject
        if gene_name == ob.gene_symbol.lower() and ob.fish_name == "WT":
            add = True
            if organ is not None and with_parent:
                if get_parent_structure(organ).name != ob.parent_structure.name:
                    add = False
            elif organ is not None and not with_parent:
                if organ.lower() != ob.super_structure.name:
                    add = False

            if add:
                start_stage.update({ob.start_stage.time})
                end_stage.update({ob.end_stage.time})
                start_index.update({ob.start_stage.index})
                end_index.update({ob.end_stage.index})

    labels_start = []
    labels_end = []
    t_count_start = []
    t_count_end = []
    index_start = []
    index_end = []
    no_of_time_span = 30
    for i in start_stage.most_common(no_of_time_span):
        labels_start.append(i[0])
        t_count_start.append(i[1])
    for i in start_index.most_common(no_of_time_span):
        index_start.append(i[0])

    for i in end_stage.most_common(no_of_time_span):
        labels_end.append(i[0])
        t_count_end.append(i[1])
    for i in end_index.most_common(no_of_time_span):
        index_end.append(i[0])

    combined_list = list(set().union(index_start, index_end))
    combined_list = sorted(combined_list)

    corrected_start_value = []
    corrected_end_value = []
    corrected_labels = []

    for i in combined_list:
        try:
            corrected_start_value.append(t_count_start[index_start.index(i)])
        except ValueError:
            corrected_start_value.append(0)

        try:
            corrected_end_value.append(t_count_end[index_end.index(i)])
        except ValueError:
            corrected_end_value.append(0)

        try:
            corrected_labels.append(labels_start[index_start.index(i)])
        except ValueError:
            corrected_labels.append(labels_end[index_end.index(i)])

    figure = plt.figure()
    ax = figure.add_subplot(111)
    ind = np.arange(len(corrected_labels))  # the x locations for the groups
    width = 0.35  # the width of the bars

    # labels = ['\n'.join(wrap(l, 15)) for l in labels]
    ax.barh(ind, corrected_start_value, width, color="#e4adea",
            label="expression starts")
    ax.barh(ind + width, corrected_end_value, width, color="#9320a2",
            label="expression ends")

    ax.set_yticks(ind + width / 2)
    ax.set_yticklabels(corrected_labels)
    ax.set_xlabel("number of literature reports\n(6 July 2018, ZFIN database)")
    ax.set_ylabel("time post fertilization (hours)")
    if organ is None:
        ax.set_title("Expression profile of $\\bf{ %s }$\n(only top %d from "
                     "literature)" % (gene_name, no_of_time_span))
    elif with_parent:
        ax.set_title("Expression profile of $\\bf{ %s }$ in %s \n(only top %d "
                     "from literature)" % (
                         gene_name, get_parent_structure(organ).name,
                         no_of_time_span))
    elif not with_parent:
        ax.set_title("Expression profile of $\\bf{ %s }$ in %s \n(only top %d "
                     "from literature)" % (gene_name, organ, no_of_time_span))

    plt.legend(loc=0)
    plt.grid(linestyle='-', alpha=0.5)
    plt.show()


expression_profile("gata4", "heart")
# check_hist()
# genes_in_organ("cardiac ventricle")
# localization("zic3", False)
