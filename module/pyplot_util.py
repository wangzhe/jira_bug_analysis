import matplotlib

matplotlib.use('Agg')

import io
import matplotlib.pyplot as plt
import numpy as np


def save_to_mime_img(filename):
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    binary_img = buf.getvalue()
    buf.close()
    # if JiraInfo().instance.is_debug():
    #     save_image(filename, binary_img)
    # plt.show()
    return binary_img


def generate_bar_chart(label, data, filename=None):
    ind = np.arange(len(data))
    fig, ax = plt.subplots()
    rects = ax.bar(ind, data, width=0.5)

    ax.set_title('Online Bug Summary')
    ax.set_ylabel("Count", fontsize=8)
    ax.set_xticks(ind)
    ax.set_xticklabels(label, fontsize=8)

    highest = max(data)
    for rect, i in zip(rects, data):
        ax.text(rect.get_x() + rect.get_width() / 2, i + highest * 0.02, str(i), color='black', ha='center',
                fontweight='bold', fontsize=8)
    return save_to_mime_img(filename)


def generate_barh_chart(label, data, filename=None):
    ind = np.arange(len(data))
    fig, ax = plt.subplots()
    rects = ax.barh(ind, data, height=0.5)

    ax.set_title('Priority')
    ax.set_xlabel("Count", fontsize=8)
    ax.set_ylabel("Level", fontsize=8)
    ax.set_yticks(ind)
    ax.set_yticklabels(label, fontsize=8)

    highest = max(data)
    for rect, i in zip(rects, data):
        ax.text(i + highest * 0.03, rect.get_y() + rect.get_height() / 2, str(i), color='black', ha='center',
                fontweight='bold', fontsize=8)
    return save_to_mime_img(filename)


def generate_pie_chart(label, data, filename=None, title='No-Title'):
    plt.clf()
    plt.title(title)

    label_with_num = [str(label[i]) + "(" + str(data[i]) + ")" for i in range(len(label))]
    patches, texts, autotexts = plt.pie(data, labels=label_with_num, autopct='%1.1f%%')
    [_.set_fontsize(8) for _ in texts]
    [_.set_fontsize(8) for _ in autotexts]

    plt.axis('equal')
    return save_to_mime_img(filename)


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
