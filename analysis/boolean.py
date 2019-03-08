import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

TIME_STEPS = 10


def get_initial_condition():
    nkx2_5 = 1
    gata5 = 1
    gata6 = 1
    tbx20 = 1
    smad9 = 1
    ext = 1
    target_gene = 0
    return [nkx2_5, gata5, gata6, tbx20, smad9, ext, target_gene]


def calculate_next(current_state: list):
    nkx2_5, gata5, gata6, tbx20, smad9, ext, target = current_state

    nkx2_5 = (gata5 and gata6) or tbx20 or smad9
    gata5 = nkx2_5
    gata6 = nkx2_5
    smad9 = ext
    tbx20 = ext
    target = nkx2_5

    return [nkx2_5, gata5, gata6, tbx20, smad9, ext, target]


def show_stable_state():
    labels = ["nkx2_5", "gata5", "gata6", "tbx20", "smad9", "ext", "target_gene"]
    expected_pattern = [1] * len(labels)
    expected_pattern[labels.index("target_gene")] = 0
    all_states = [get_initial_condition()]
    for i in range(TIME_STEPS):
        all_states.append(calculate_next(all_states[-1]))

    all_states.append(expected_pattern)
    p = np.asanyarray(all_states)
    p = p.transpose()
    mask = p * 0
    mask_start = p * 0
    mask_output = p * 0
    mask[:, -1] = 1
    mask_start[:, 0] = 1
    mask_output[:, -2] = 1
    cmap = "tab20c_r"
    ax = sns.heatmap(p, cmap=cmap, cbar=False)
    sns.heatmap(p, cmap=cmap, mask=mask_start != 1, annot=True, cbar=False)
    sns.heatmap(p, cmap=cmap, mask=mask_output != 1, annot=True, cbar=False)
    sns.heatmap(p, mask=mask != 1, cmap="Blues", annot=True, cbar=False)

    for i in range(TIME_STEPS + 1):
        if i == 1:
            ax.axvline(x=1, color='k', linestyle="--")
        elif i == TIME_STEPS:
            ax.axvline(x=TIME_STEPS, color='k', linestyle="--")
        else:
            ax.axvline(x=i, color='white', alpha=0.3)
    plt.yticks(rotation=0)
    plt.xticks([])
    plt.xlabel("Arbitrary Time Steps")
    plt.ylabel("TRN Components")
    ax.set_yticklabels(labels)
    plt.savefig("plot.png", format='png', dpi=300, bbox_inches='tight')
    plt.show()


def run():
    show_stable_state()
