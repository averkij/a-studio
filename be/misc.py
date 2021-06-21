"""Misc helper functions"""

import glob
import json
import logging
import os
import pathlib
import pickle
import sqlite3
import sys
from warnings import simplefilter

import config
import constants as con
import user_db_helper


def get_files_list(folder, mask="*.txt"):
    """Get file names list by mask"""
    return [os.path.basename(x) for x in get_files_list_with_path(folder, mask)]


def get_files_list_with_path(folder, mask="*.txt"):
    """Get file paths list by mask"""
    if not os.path.isdir(folder):
        return []
    return glob.glob("{0}/{1}".format(folder, mask))


def get_processing_list_with_state(username, lang_from, lang_to):
    """Get processing docs list with states"""
    res = []
    for guid, name, guid_from, guid_to, state_code, done_batches, total_batches in user_db_helper.get_alignments_list(username, lang_from, lang_to):
        res.append({
            "guid": guid,
            "name": name,
            "guid_from": guid_from,
            "guid_to": guid_to,
            "state": (state_code, total_batches, done_batches),
            # "imgs": get_files_list(os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER, username), mask=f"{guid}.best_*.png"),
            # "sim_grades": get_sim_grades(file)
        })
    return res


def get_raw_files(username, lang_code):
    """Get uploaded raw files list"""
    res = []
    for file, guid, _ in user_db_helper.get_documents_list(username, lang_code):
        res.append({
            "name": file,
            "guid": guid,
            "has_proxy": os.path.isfile(os.path.join(con.UPLOAD_FOLDER, username, con.PROXY_FOLDER, lang_code, file))
        })
    return res


def get_sim_grades(processing_file):
    """Get saved similarity grades"""
    docs = pickle.load(open(processing_file, "rb"))
    return docs["sim_grades"]


def clean_img_user_foler(username, align_guid):
    """Clean user folder with images"""
    imgs = get_files_list_with_path(os.path.join(
        con.STATIC_FOLDER, con.IMG_FOLDER, username), mask=f"{align_guid}.best_*.png")
    for img in imgs:
        if os.path.isfile(img):
            os.remove(img)


def create_folders(username, lang):
    """Create folders for a new user"""
    if username and lang:
        pathlib.Path(os.path.join(con.STATIC_FOLDER, con.IMG_FOLDER, username)).mkdir(
            parents=True, exist_ok=True)
        pathlib.Path(os.path.join(con.UPLOAD_FOLDER, username,
                                  con.RAW_FOLDER, lang)).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(con.UPLOAD_FOLDER, username,
                                  con.SPLITTED_FOLDER, lang)).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(con.UPLOAD_FOLDER, username,
                                  con.PROXY_FOLDER, lang)).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(con.UPLOAD_FOLDER, username,
                                  con.NGRAM_FOLDER, lang)).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(con.UPLOAD_FOLDER, username,
                                  con.PROCESSING_FOLDER, lang)).mkdir(parents=True, exist_ok=True)
        pathlib.Path(os.path.join(con.UPLOAD_FOLDER, username,
                                  con.DONE_FOLDER, lang)).mkdir(parents=True, exist_ok=True)


def get_texts_length(db_path):
    """Get splitted lines count"""
    res = []

    with sqlite3.connect(db_path) as db:
        cur = db.execute(
            '''SELECT
                (select count(*) as len1 from splitted_from),
                (select count(*) as len2 from splitted_to)
            '''
        )
        res = (cur.fetchone())
    return res


def get_filename(username, guid):
    """Get filename by id"""
    filename = [x[0] for x in user_db_helper.get_documents_list(
        username) if x[1] == guid]
    return filename[0] if filename else None


def get_fileinfo(username, guid):
    """Get file info by id"""
    filename = [(x[0], x[2]) for x in user_db_helper.get_documents_list(
        username) if x[1] == guid]
    return filename[0] if filename else None


def check_folder(folder):
    """Check if folder exists"""
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)


def check_file(folder, files, file_id):
    """Check if file exists"""
    if len(files) < file_id+1:
        logging.debug(
            f"Document with id={file_id} not found. folder: {folder}")
        return False
    processing_file = os.path.join(folder, files[file_id])
    if not os.path.isfile(processing_file):
        logging.debug(f"Document {processing_file} not found.")
        return False
    return True


def get_batch(iter1, iter2, iter3, n):
    """Get batch"""
    l1 = len(iter1)
    l3 = len(iter3)
    k = int(round(n * l3/l1))
    kdx = 0 - k
    for ndx in range(0, l1, n):
        kdx += k
        yield iter1[ndx:min(ndx + n, l1)], iter2[kdx:min(kdx + k, l3)], iter3[kdx:min(kdx + k, l3)]


def get_batch_intersected(iter1, iter2, batch_ids, batch_shift=0, n=config.DEFAULT_BATCHSIZE, window=config.DEFAULT_WINDOW):
    """Get batch with an additional window"""
    l1 = len(iter1)
    l2 = len(iter2)
    k = int(round(n * l2/l1))
    kdx = 0 - k

    if k < window*2:
        # subbatches will be intersected
        logging.warning(
            f"Batch for the second language is too small. k = {k}, window = {window}")

    counter = 0
    for ndx in range(0, l1, n):
        kdx += k
        if counter in batch_ids:
            yield iter1[ndx:min(ndx + n, l1)], \
                iter2[max(0, kdx - window + batch_shift):min(kdx + k + window + batch_shift, l2)], \
                list(range(ndx, min(ndx + n, l1))), \
                list(range(max(0, kdx - window + batch_shift), min(kdx + k + window + batch_shift, l2))), \
                counter
        counter += 1


def try_parse_int(value):
    """Try parse int"""
    try:
        return int(value), True
    except ValueError:
        return value, False


def parse_json_array(json_str):
    """Parse JSON string array"""
    if not json_str:
        return []
    try:
        return json.loads(json_str)
    except:
        return []


def configure_logging(level=logging.INFO):
    """"Configure logging module"""
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    simplefilter(action='ignore', category=FutureWarning)
    # logging.basicConfig(level=level, filename='app.log', filemode='a', format='%(asctime)s [%(levelname)s] - %(process)d: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.basicConfig(stream=sys.stdout, level=level, filemode='a',
                        format='%(asctime)s [%(levelname)s] - %(process)d: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.getLogger('matplotlib.font_manager').disabled = True


def lazy_property(func):
    """"Lazy initialization attribute"""
    attr_name = '_lazy_' + func.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return _lazy_property
