import matplotlib.pyplot as plt
from module.sys_invariant import graphic_path


def generate_bar_chart(x, y, filename=None):
    plt.title('Online Bug Summary')
    plt.xlabel("Date", fontsize=8)
    plt.ylabel("Count", fontsize=8)

    highest = max(y)
    for v, i in zip(x, y):
        plt.text(v, i + highest * 0.02, str(i), color='black', ha='center', fontweight='bold', fontsize=8)
    plt.bar(x, y, width=0.5)
    if filename is not None:
        plt.savefig(graphic_path + filename)
    # plt.show()
