"""Visualization helper"""

import json
import logging
import os

import numpy as np
from lingtrain_aligner import helper
from matplotlib import pyplot as plt


def visualize_alignment_by_db(db_path, output_path, lang_name_from="ru", lang_name_to="de", batch_size=0, size=(260, 300), batch_ids=[], plt_show=False, transparent_bg=False, plot_batch_info=False):
    """Visualize alignment using ids from the database"""
    if batch_size > 0:
        index = helper.get_clear_flatten_doc_index(db_path)
        xs, ys = [], []
        for i, ix in enumerate(index):
            from_ids, to_ids = json.loads(ix[1]), json.loads(ix[3])
            for from_id in from_ids:
                for to_id in to_ids:
                    xs.append(from_id)
                    ys.append(to_id)

        x_max, y_max = max(xs), max(ys)
        is_last = x_max % batch_size > 0
        total_batches = x_max//batch_size + (1 if is_last else 0)
        batches = [[[], []] for _ in range(total_batches)]

        for x, y in zip(xs, ys):
            batch_id = (x-1) // batch_size
            batches[batch_id][0].append(x)
            batches[batch_id][1].append(y)
    else:
        index = helper.get_doc_index_original(db_path)
        batches = [[[], []] for _ in range(len(index))]
        for i, batch in enumerate(index):
            xs, ys = [], []
            for ix in batch:
                from_ids, to_ids = json.loads(ix[1]), json.loads(ix[3])
                for from_id in from_ids:
                    for to_id in to_ids:
                        xs.append(from_id)
                        ys.append(to_id)
            for x, y in zip(xs, ys):
                batches[i][0].append(x)
                batches[i][1].append(y)

    if len(batch_ids) == 1 and batch_ids[0] == -1:
        batch_ids = []

    for i, batch in enumerate(batches):
        if i in batch_ids or len(batch_ids) == 0:
            y_min, x_min = min(batch[0]), min(batch[1])
            y_max, x_max = max(batch[0]), max(batch[1])
            align_matrix = np.zeros((y_max-y_min, x_max-x_min))
            try:
                for y, x in zip(batch[0], batch[1]):
                    align_matrix[y-y_min - 1, x-x_min - 1] = 1
                shift, window = None, None
                if plot_batch_info:
                    shift, window = helper.get_batch_info(db_path, i)
                save_pic(align_matrix, lang_name_to, lang_name_from,
                        output_path, batch_number=i, interval_x=(x_min, x_max), interval_y=(y_min, y_max), size=size, plt_show=plt_show, transparent=transparent_bg, shift=shift, window=window)
            except Exception as e:
                logging.error(e, exc_info=True)


def save_pic(align_matrix, lang_name_to, lang_name_from, output_path, batch_number, interval_x, interval_y, size=(260, 260), plt_show=False, transparent=False, shift=None, window=None):
    """Save the resulted picture"""
    output = "{0}_{1}{2}".format(os.path.splitext(output_path)[
                                 0], batch_number, os.path.splitext(output_path)[1])
    my_dpi = 100
    plt.figure(figsize=(size[0]/my_dpi, size[1]/my_dpi), dpi=my_dpi)    

    #plot linear regression
    batch_info = restore_batch_info(align_matrix)
    x = np.array(batch_info[1])
    y = np.array(batch_info[0])
    coefs, res, rank, s_val, cond = np.polyfit(x, y, 1, full=True)
    m, b = coefs[0], coefs[1]
    plt.plot(x, m*x + b, c="red", linewidth=0.5)

    #plot alignment
    plt.imshow(align_matrix, cmap='Greens', interpolation='nearest')
    plt.xlabel(lang_name_to, fontsize=12, labelpad=-18)
    plt.ylabel(lang_name_from, fontsize=12, labelpad=-18)
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=False, right=False, left=False, labelleft=False)

    #plot info
    if shift is not None and window is not None:
        plt.text(0.0, -0.09, f"s={shift}, w={window}, e={np.sqrt(res[0]):.2f}", fontsize = 9, transform=plt.gca().transAxes, c="black")
        plt.text(0.0, -0.18, f"{lang_name_to}=[{interval_x[0]}; {interval_x[1]}], {lang_name_from}=[{interval_y[0]}; {interval_y[1]}]", fontsize = 9, transform=plt.gca().transAxes, c="black")
        
    plt.savefig(output, dpi=my_dpi, transparent=transparent)  
    # plt.savefig(output, bbox_inches="tight", pad_inches=0, dpi=my_dpi)
    if plt_show:
        plt.show()
    plt.close()


def restore_batch_info(m):
    x, y = [], []
    for i, _ in enumerate(m):
        for j, val in enumerate(m[i]):
            if val==1:
                x.append(j+1)
                y.append(i+1)
    return y,x
