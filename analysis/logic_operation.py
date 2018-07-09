"""
Logic Operations
"""
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns

TIME_STEPS = 20

labels = ["nkx2_5", "gata4", "gata5", "gata6", "fgf8a", "bmp4", "foxc1",
          "foxa2", "hand2", "tbx5a", "mef2ca", "myl7", "ptx2", "smad2", "tdgf1",
          "zic3", "external"]

expected_pattern = [True] * len(labels)
expected_pattern[labels.index("gata4")] = False
expected_pattern[labels.index("gata6")] = False
expected_pattern[labels.index("fgf8a")] = False
expected_pattern[labels.index("ptx2")] = False


class SystemParameters:
    def __init__(self, external):
        self.nkx2_5 = True
        self.gata4 = True
        self.gata5 = True
        self.gata6 = True
        self.fgf8a = True
        self.bmp4 = True
        self.foxc1 = True
        self.foxa2 = True
        self.hand2 = True
        self.tbx5a = True
        self.mef2ca = True
        self.myl7 = True
        self.ptx2 = False
        self.smad2 = True
        self.tdgf1 = True
        self.zic3 = False
        self.external = external
        self.previous_state = []
        self.save_state()

    @property
    def current_state(self):
        return [self.nkx2_5, self.gata4, self.gata5, self.gata6,
                self.fgf8a, self.bmp4, self.foxc1, self.foxa2,
                self.hand2, self.tbx5a, self.mef2ca,
                self.myl7, self.ptx2, self.smad2, self.tdgf1,
                self.zic3, self.external]

    def save_state(self):
        self.previous_state = self.current_state

    def is_next_available(self) -> bool:
        return not (self.previous_state == self.current_state)

    def next(self):
        self.save_state()
        a = self.foxa2 and self.bmp4 and self.foxc1 \
            and self.gata4 and (self.gata5 or self.gata6)
        nkx2_5 = a and self.fgf8a

        gata4 = self.nkx2_5
        foxa2 = self.smad2 or self.zic3
        hand2 = self.nkx2_5 or self.gata4
        tbx5a = self.nkx2_5
        mef2ca = self.nkx2_5 or self.gata4
        myl7 = self.nkx2_5
        ptx2 = self.smad2 and self.zic3
        smad2 = self.tdgf1
        tdgf1 = self.zic3 or self.external

        self.nkx2_5 = nkx2_5
        self.gata4 = gata4
        self.foxa2 = foxa2
        self.hand2 = hand2
        self.tbx5a = tbx5a
        self.mef2ca = mef2ca
        self.myl7 = myl7
        self.ptx2 = ptx2
        self.smad2 = smad2
        self.tdgf1 = tdgf1


def solve_logic():
    state = SystemParameters(True)
    p = [state.current_state]
    for i in range(TIME_STEPS):
        state.next()
        p.append(state.current_state)

    p.append(expected_pattern)
    p = np.asanyarray(p)
    p = p.transpose()

    mask = p * 0
    mask_start = p * 0
    mask_output = p * 0
    mask[:, -1] = 1
    mask_start[:, 0] = 1
    mask_output[:, -2] = 1
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    cmap = "tab20c_r"
    ax = sns.heatmap(p, cmap=cmap, cbar=False)
    sns.heatmap(p, cmap=cmap, mask=mask_start != 1, annot=True, cbar=False)
    sns.heatmap(p, cmap=cmap, mask=mask_output != 1, annot=True, cbar=False)
    sns.heatmap(p, mask=mask != 1, cmap="Blues", annot=True, cbar=False)
    ax.axvline(x=1, color='k', linestyle="--")
    ax.axvline(x=TIME_STEPS, color='k', linestyle="--")
    plt.yticks(rotation=0)
    plt.xticks([])
    plt.xlabel("Time Step")
    plt.ylabel("TRN Components")
    ax.set_yticklabels(labels)
    plt.savefig("plot.png", format='png', dpi=300, bbox_inches='tight')
    plt.show()
