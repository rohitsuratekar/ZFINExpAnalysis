"""
Rohit Suratekar
March 2019

Visualization functions
"""
import matplotlib.pyplot as plt
from SecretColors import palette

from analysis.basic import get_expression_pattern_in


def plot_expression_profile(gene: str, parent_structure: str = None):
    p = palette.Palette()
    entries_start = []

    for d in get_expression_pattern_in(gene, parent_structure):
        entries_start.append(float(d.start_stage.time))

    plt.hist(entries_start, color=p.cerulean())
    plt.ylabel("Frequency of Publications")
    plt.xlabel("hpf")
    plt.title("'{0}' Expression Star Stage".format(gene))
    plt.show()


def plot_expression_at_24_48(gene: str, parent_structure: str = None):
    p = palette.Palette()
    entries_start = []

    for d in get_expression_pattern_in(gene, parent_structure):
        if float(d.start_stage.time) in [24, 48]:
            entries_start.append(float(d.start_stage.time))

    plt.hist(entries_start, color=p.cerulean())
    plt.ylabel("Frequency of Publications")
    plt.xlabel("hpf")
    plt.title("'{0}' Expression at 24 and 48 hpf".format(gene))
    plt.show()


def run():
    plot_expression_at_24_48("nkx2.5", "heart")
