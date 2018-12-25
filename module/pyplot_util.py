import io

import matplotlib.pyplot as plt

from module.storage_util import save_image
from module.sys_invariant import need_show_plot


def save_to_storage(filename):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    save_image(filename, buf)
    buf.close()

    if need_show_plot:
        plt.show()


def generate_bar_chart(label, data, filename=None):
    plt.clf()
    plt.title('Online Bug Summary')
    plt.xlabel("Date", fontsize=8)
    plt.ylabel("Count", fontsize=8)

    highest = max(data)
    for v, i in zip(label, data):
        plt.text(v, i + highest * 0.02, str(i), color='black', ha='center', fontweight='bold', fontsize=8)
    plt.bar(label, data, width=0.5)
    save_to_storage(filename)


def generate_barh_chart(label, data, filename=None):
    plt.clf()
    plt.title('Priority')
    plt.xlabel("Count", fontsize=8)
    plt.ylabel("Level", fontsize=8)

    highest = max(data)
    for v, i in zip(label, data):
        plt.text(i + highest * 0.01, v, str(i), color='black', va='center', fontweight='bold', fontsize=8)
    plt.barh(label, data, height=0.5)
    save_to_storage(filename)


def generate_pie_chart(label, data, filename=None, title='No-Title'):
    plt.clf()
    plt.title(title)

    label_with_num = [str(label[i]) + "(" + str(data[i]) + ")" for i in range(len(label))]
    patches, texts, autotexts = plt.pie(data, labels=label_with_num, autopct='%1.1f%%')
    [_.set_fontsize(8) for _ in texts]
    [_.set_fontsize(8) for _ in autotexts]

    plt.axis('equal')
    save_to_storage(filename)


def bug_data_and_label_classified_in_catalog(bug_list, bug_label, bug_catalog):
    bug_data_in_catalog = []
    bug_classified_data_in_catalog = []
    for bug in bug_list.bugs:
        if bug[bug_catalog] is None:
            continue
        bug_data_in_catalog.append(bug[bug_catalog])
    for var in bug_label:
        bug_classified_data_in_catalog.append(bug_data_in_catalog.count(var))
    return bug_classified_data_in_catalog, bug_label
