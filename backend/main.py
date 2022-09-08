"""Main module"""

import datetime
import logging
import os
import tempfile
import uuid

import config
import constants as con
import editor
import editor_helper
import main_db_helper
import misc
import user_db_helper
from align_processor import AlignmentProcessor
from flask import Flask, abort, request, send_file
from flask_cors import CORS
from lingtrain_aligner import (
    aligner,
    helper,
    preprocessor,
    splitter,
    saver,
    resolver,
    reader,
    vis_helper,
    constants as la_con,
)

misc.configure_logging()


# from mlflow import log_metric

app = Flask(__name__)
CORS(app)


@app.route("/items/<username>/init", methods=["GET"])
def init_userspace(username):
    """Prepare user workspace"""
    main_db_helper.init_main_db()
    user_db_helper.init_user_db(username)
    return ("", 200)


@app.route("/items/<username>/raw/<lang>", methods=["GET", "POST"])
def items(username, lang):
    """Get uploaded user raw documents"""

    # TODO add language code validation
    misc.create_folders(username, lang)
    # load documents
    if request.method == "POST":
        if lang in request.files:
            file = request.files[lang]
            upload_folder = con.RAW_FOLDER
            filename = file.filename
            direction = request.form.get("direction", "from")

            if request.form["type"] != "proxy" and user_db_helper.file_exists(
                username, lang, filename
            ):
                return ("File already exists", 400)

            if request.form["type"] == "proxy":
                align_guid = request.form.get("align_guid", "")
                _, guid_from, guid_to, _, _, _ = user_db_helper.get_alignment_info(
                    username, align_guid
                )
                filename_from, lang_from = user_db_helper.get_document_info(
                    username, guid_from
                )
                filename_to, lang_to = user_db_helper.get_document_info(
                    username, guid_to
                )
                db_folder = os.path.join(
                    con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
                )
                db_path = os.path.join(db_folder, f"{align_guid}.db")
                upload_folder = con.PROXY_FOLDER
                filename = filename_from if direction == "from" else filename_to
            else:
                user_db_helper.register_file(username, lang, filename)

            logging.info(f"[{username}]. Loading document {file.filename}.")
            upload_path = os.path.join(
                con.UPLOAD_FOLDER, username, upload_folder, lang, filename
            )
            file.save(upload_path)

            if request.form["type"] == "raw":
                raw_path = os.path.join(
                    con.UPLOAD_FOLDER, username, con.RAW_FOLDER, lang, filename
                )
                splitted_path = os.path.join(
                    con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang, filename
                )
                splitter.split_by_sentences_and_save(
                    raw_path, splitted_path, lang, handle_marks=True
                )
            elif request.form["type"] == "proxy":
                logging.info(
                    f"[{username}]. Update proxy. {upload_path} into {db_path} database."
                )
                aligner.load_proxy(db_path, upload_path, direction)
                user_db_helper.update_alignment_proxy_loaded(
                    username, align_guid, direction
                )

            logging.info(f"[{username}]. Success. {filename} is loaded.")
        return ("", 200)
    # return documents list
    files = {"items": {lang: misc.get_raw_files(username, lang)}}
    return files


@app.route("/items/<username>/splitted/<lang>/<guid>/download", methods=["GET"])
def download_splitted(username, lang, guid):
    """Download splitted document file"""
    logging.info(f"[{username}]. Downloading {lang} {guid} splitted document.")
    filename = misc.get_filename(username, guid)
    if not filename:
        abort(404)
    path = os.path.join(
        con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang, filename
    )
    if not os.path.isfile(path):
        abort(404)
    logging.info(f"[{username}]. Document found. Path: {path}. Sent to user.")
    return send_file(path)


@app.route(
    "/items/<username>/splitted/<lang>/<guid>/<int:count>/<int:page>", methods=["GET"]
)
def get_splitted(username, lang, guid, count, page):
    """Get splitted document page"""
    filename = misc.get_filename(username, guid)
    if not filename:
        return {"items": {lang: []}}
    path = os.path.join(
        con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang, filename
    )
    if not os.path.isfile(path):
        return {"items": {lang: []}}

    lines = []
    lines_count = 0
    symbols_count = 0
    shift = (page - 1) * count

    with open(path, mode="r", encoding="utf-8") as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break
            lines_count += 1
            symbols_count += len(line)
            if count > 0 and (lines_count <= shift or lines_count > shift + count):
                continue
            line = preprocessor.parse_marked_line(line.strip())
            lines.append((line, lines_count))

    total_pages = (lines_count // count) + (1 if lines_count % count != 0 else 0)
    meta = {
        "lines_count": lines_count - 1,
        "symbols_count": symbols_count,
        "page": page,
        "total_pages": total_pages,
    }
    return {"items": {lang: lines}, "meta": {lang: meta}}


@app.route("/items/<username>/marks/<lang>/<guid>", methods=["GET"])
def get_marks(username, lang, guid):
    """Get document marks"""
    filename = misc.get_filename(username, guid)
    if not filename:
        return {"items": {lang: []}}
    path = os.path.join(
        con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang, filename
    )
    if not os.path.isfile(path):
        return {"items": {lang: []}}
    marks = []
    with open(path, mode="r", encoding="utf-8") as input_file:
        lines = input_file.readlines()
        for i, line in enumerate(lines):
            preprocessor.extract_marks(marks, line.strip(), i)
    return {"items": marks}


@app.route("/items/<username>/alignment/marks/<align_guid>", methods=["GET"])
def get_alignment_marks(username, align_guid):
    """Get alignment marks"""
    if not user_db_helper.alignment_guid_exists(username, align_guid):
        return ("", 400)
    logging.info(f"get_alignment_marks parameters: align_guid {align_guid}")

    _, guid_from, guid_to, _, _, _ = user_db_helper.get_alignment_info(
        username, align_guid
    )
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")

    meta_dict = helper.get_meta_dict(db_path)
    res = {"items": {lang_from: [], lang_to: []}}

    for mark_name in meta_dict:
        for mark_tuple in meta_dict[mark_name]:
            # (val, occurence, par_id, id)
            val = mark_tuple[0]
            idx = mark_tuple[1]
            pid = mark_tuple[2]
            id = mark_tuple[3]
            if mark_name.endswith("from"):
                res["items"][lang_from].append(
                    (val, idx, mark_name[: len(mark_name) - 5], pid, id)
                )
            else:
                res["items"][lang_to].append(
                    (val, idx, mark_name[: len(mark_name) - 3], pid, id)
                )

    return res


@app.route("/items/<username>/alignment/marks/<align_guid>/add", methods=["POST"])
def add_alignment_mark(username, align_guid):
    """Get alignment marks"""
    if not user_db_helper.alignment_guid_exists(username, align_guid):
        return ("", 400)

    _, guid_from, guid_to, _, _, _ = user_db_helper.get_alignment_info(
        username, align_guid
    )
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")

    mark = request.form.get("type", "")
    val_from = request.form.get("valFrom", "")
    val_to = request.form.get("valTo", "")
    par_id_from, _ = misc.try_parse_int(request.form.get("parIdFrom", -1))
    par_id_to, _ = misc.try_parse_int(request.form.get("parIdTo", -1))
    # TODO occurence parameter

    logging.info(
        f"get_alignment_marks parameters: align_guid: {align_guid} mark: {mark} val_from: {val_from} val_to: {val_to}, parIdFrom: {par_id_from}, parIdTo: {par_id_to}"
    )

    if (
        mark in preprocessor.MARKS_FOR_ADDING
        and val_from
        and val_to
        and par_id_from >= 0
        and par_id_to >= 0
    ):
        helper.add_meta(db_path, mark, val_from, val_to, par_id_from, par_id_to)
    else:
        return ("invalid parameters", 400)

    return ("", 200)


@app.route("/items/<username>/alignment/marks/<align_guid>/bulkadd", methods=["POST"])
def bulk_add_alignment_mark(username, align_guid):
    """Get alignment marks"""
    if not user_db_helper.alignment_guid_exists(username, align_guid):
        return ("", 400)

    _, guid_from, guid_to, _, _, _ = user_db_helper.get_alignment_info(
        username, align_guid
    )
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")

    raw_info = request.form.get("rawInfo", "")

    if raw_info:
        text_info = raw_info.split("\n")
        info = [
            (x.split(",")[0], x.split(",")[1], x.split(",")[2])
            for x in text_info
            if len(x.split(",")) > 2
        ]
        info.sort(key=lambda x: x[1])
        for i in range(0, len(info), 2):
            if i + 1 < len(info):
                helper.add_meta(
                    db_path,
                    preprocessor.IMAGE,
                    info[i][0],
                    info[i + 1][0],
                    info[i][1],
                    info[i + 1][1],
                    info[i][2],
                    info[i + 1][2],
                )
    else:
        return ("invalid parameters", 400)

    return ("", 200)


@app.route("/items/<username>/alignment/marks/<align_guid>/edit", methods=["POST"])
def edit_alignment_mark(username, align_guid):
    """Get alignment marks"""
    if not user_db_helper.alignment_guid_exists(username, align_guid):
        return ("", 400)

    _, guid_from, guid_to, _, _, _ = user_db_helper.get_alignment_info(
        username, align_guid
    )
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")

    mark_id, _ = misc.try_parse_int(request.form.get("mark_id", -1))
    operation = request.form.get("operation", "")

    if mark_id > 0 and operation == "delete":
        logging.info(f"deleting mark: align_guid: {align_guid}, mark_id: {mark_id}")
        helper.delete_meta(db_path, mark_id)
        return ("", 200)

    direction = request.form.get("direction", "")
    type = request.form.get("type", "")
    val = request.form.get("value", "")
    par_id, _ = misc.try_parse_int(request.form.get("par_id", -1))
    # TODO occurence parameter

    logging.info(
        f"get_alignment_marks parameters: align_guid: {align_guid}, mark_id: {mark_id}, val: {val}, parId: {par_id}"
    )

    if operation == "edit" and val and par_id >= 0 and mark_id > 0:
        helper.edit_meta(db_path, type, direction, mark_id, par_id, val)
    else:
        return ("invalid parameters", 400)

    return ("", 200)


@app.route("/items/<username>/alignment/create", methods=["POST"])
def create_alignment(username):
    """Register new alignment"""
    id_from = request.form.get("id_from", "")
    id_to = request.form.get("id_to", "")
    name = request.form.get("name", "")

    if user_db_helper.alignment_exists(username, id_from, id_to):
        return ("", 200)

    if not user_db_helper.file_exists_by_guid(
        username, id_from
    ) or not user_db_helper.file_exists_by_guid(username, id_to):
        return ("", 400)

    batch_size = config.DEFAULT_BATCHSIZE
    file_from, lang_from = misc.get_fileinfo(username, id_from)
    file_to, lang_to = misc.get_fileinfo(username, id_to)

    splitted_from = os.path.join(
        con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang_from, file_from
    )
    splitted_to = os.path.join(
        con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang_to, file_to
    )
    proxy_to = os.path.join(
        con.UPLOAD_FOLDER, username, con.PROXY_FOLDER, lang_to, file_to
    )
    proxy_from = os.path.join(
        con.UPLOAD_FOLDER, username, con.PROXY_FOLDER, lang_from, file_from
    )

    align_guid = uuid.uuid4().hex
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")

    misc.check_folder(db_folder)

    with open(splitted_from, "r", encoding="utf8") as input_from:
        lines_from = input_from.readlines()
    with open(splitted_to, "r", encoding="utf8") as input_to:
        lines_to = input_to.readlines()

    lines_proxy_from, lines_proxy_to = [], []
    if os.path.isfile(proxy_from):
        with open(proxy_from, "r", encoding="utf8") as input_proxy_from:
            lines_proxy_from = input_proxy_from.readlines()
    if os.path.isfile(proxy_to):
        with open(proxy_to, "r", encoding="utf8") as input_proxy_to:
            lines_proxy_to = input_proxy_to.readlines()

    aligner.fill_db(
        db_path,
        lang_from,
        lang_to,
        lines_from,
        lines_to,
        lines_proxy_from,
        lines_proxy_to,
    )

    len_from, _ = misc.get_texts_length(db_path)

    is_last = len_from % batch_size > 0
    total_batches = len_from // batch_size + 1 if is_last else len_from // batch_size
    if config.TEST_RESTRICTION_MAX_BATCHES > 0:
        total_batches = min(config.TEST_RESTRICTION_MAX_BATCHES, total_batches)

    user_db_helper.register_alignment(
        username, lang_from, lang_to, align_guid, id_from, id_to, name, total_batches
    )

    return ("", 200)


@app.route("/items/<username>/alignment/delete", methods=["POST"])
def delete_alignment(username):
    """Mark existed alignment as deleted"""
    align_guid = request.form.get("align_guid", "")

    if not user_db_helper.alignment_guid_exists(username, align_guid):
        return ("", 400)

    user_db_helper.delete_alignment(username, align_guid)

    return ("", 200)


@app.route("/items/<username>/raw/delete", methods=["POST"])
def delete_document(username):
    """Delete uploaded file"""
    guid = request.form.get("guid", "")
    lang = request.form.get("lang", "")
    filename = request.form.get("filename", "")

    user_db_helper.delete_document(username, guid, lang, filename)

    return ("", 200)


@app.route("/items/<username>/alignment/visualize", methods=["POST"])
def update_visualization(username):
    """Align two splitted documents"""
    align_guid = request.form.get("id", "")
    update_all = request.form.get("update_all", "")
    batch_ids = misc.parse_json_array(request.form.get("batch_ids", "[0]"))

    logging.info(
        f"visualize parameters align_guid {align_guid} update_all {update_all} batch_ids {batch_ids}"
    )

    _, guid_from, guid_to, _, _, total_batches = user_db_helper.get_alignment_info(
        username, align_guid
    )
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")

    if update_all:
        logging.info(f"[{username}]. Cleaning images.")
        misc.clean_img_user_foler(username, align_guid)
        batch_ids = list(range(total_batches))

    # exit if batch ids is empty
    batch_ids = [x for x in batch_ids if x < total_batches][:total_batches]
    if not batch_ids:
        abort(404)

    res_img_best = os.path.join(
        con.STATIC_FOLDER, con.IMG_FOLDER, username, f"{align_guid}.best.png"
    )

    vis_helper.visualize_alignment_by_db(
        db_path,
        res_img_best,
        lang_name_from=lang_from,
        lang_name_to=lang_to,
        batch_ids=batch_ids,
        transparent_bg=True,
        show_info=config.VIS_BATCH_INFO,
        show_regression=config.VIS_REGRESSION,
    )

    return ("", 200)


@app.route("/items/<username>/alignment/align", methods=["POST"])
def start_alignment(username):
    """Align two splitted documents"""
    align_guid = request.form.get("id", "")
    align_all = request.form.get("align_all", "")
    batch_ids = misc.parse_json_array(request.form.get("batch_ids", "[0]"))
    batch_shift, _ = misc.try_parse_int(request.form.get("batch_shift", 0))
    window, _ = misc.try_parse_int(request.form.get("window", config.DEFAULT_WINDOW))
    use_proxy_from = True if request.form.get("use_proxy_from", "") == "true" else False
    use_proxy_to = True if request.form.get("use_proxy_to", "") == "true" else False

    logging.info(
        f"align parameters align_guid {align_guid} align_all {align_all} batch_ids {batch_ids}, batch_shift {batch_shift}"
    )

    (
        name,
        guid_from,
        guid_to,
        state,
        curr_batches,
        total_batches,
    ) = user_db_helper.get_alignment_info(username, align_guid)
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)

    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)

    logging.info(
        f"align parameters START align_guid {align_guid} align_all {align_all} batch_ids {batch_ids} name {name} guid_from {guid_from} guid_to {guid_to} total_batches {total_batches} use_proxy_from {use_proxy_from} use_proxy_to {use_proxy_to}"
    )

    lines_from = aligner.get_splitted_from(db_path)
    lines_to = aligner.get_splitted_to(db_path)

    proxy_from = aligner.get_proxy_from(db_path)
    proxy_to = aligner.get_proxy_to(db_path)

    logging.info(f"[{username}]. Cleaning images.")
    # misc.clean_img_user_foler(username, align_guid)

    if align_all:
        batch_ids = list(range(total_batches))

    # exit if batch ids is empty
    batch_ids = [x for x in batch_ids if x < total_batches][:total_batches]
    if not batch_ids:
        abort(404)
    if align_all:
        user_db_helper.update_alignment_state(
            user_db_path, align_guid, con.PROC_INIT, 0, total_batches
        )

    user_db_helper.update_alignment_state_by_align_id(
        user_db_path, align_guid, con.PROC_IN_PROGRESS
    )

    # parallel processing
    logging.info(f"{username}: align started")
    res_img_best = os.path.join(
        con.STATIC_FOLDER, con.IMG_FOLDER, username, f"{align_guid}.best.png"
    )

    task_list = [
        (
            lines_from_batch,
            lines_to_batch,
            proxy_from_batch,
            proxy_to_batch,
            line_ids_from,
            line_ids_to,
            batch_id,
            batch_shift,
            window,
        )
        for lines_from_batch, lines_to_batch, proxy_from_batch, proxy_to_batch, line_ids_from, line_ids_to, batch_id in aligner.get_batch_intersected(
            lines_from,
            lines_to,
            n=config.DEFAULT_BATCHSIZE,
            window=window,
            batch_ids=batch_ids,
            batch_shift=batch_shift,
            iter3=proxy_from,
            iter4=proxy_to,
        )
    ]

    proc_count = config.PROCESSORS_COUNT
    proc = AlignmentProcessor(
        proc_count,
        db_path,
        user_db_path,
        res_img_best,
        lang_from,
        lang_to,
        align_guid,
        model_name=config.MODEL,
        embed_batch_size=config.EMBED_BATCH_SIZE,
        normalize_embeddings=config.NORMALIZE_EMBEDDINGS,
        operation=la_con.OPERATION_CALCULATE_CUSTOM,
        plot_info=config.VIS_BATCH_INFO,
        plot_regression=config.VIS_REGRESSION,
        use_proxy_from=use_proxy_from,
        use_proxy_to=use_proxy_to,
    )
    proc.add_tasks(task_list)
    proc.start_align()

    return con.EMPTY_LINES


@app.route("/items/<username>/alignment/align/next", methods=["POST"])
def align_next_batch(username):
    """Align next batch of two splitted documents"""
    align_guid = request.form.get("id", "")
    amount, _ = misc.try_parse_int(request.form.get("amount", 1))
    batch_shift, _ = misc.try_parse_int(request.form.get("batch_shift", 0))
    window, _ = misc.try_parse_int(request.form.get("window", config.DEFAULT_WINDOW))
    (
        name,
        guid_from,
        guid_to,
        state,
        curr_batches,
        total_batches,
    ) = user_db_helper.get_alignment_info(username, align_guid)
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    use_proxy_from = True if request.form.get("use_proxy_from", "") == "true" else False
    use_proxy_to = True if request.form.get("use_proxy_to", "") == "true" else False

    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)

    last_batch_id = user_db_helper.get_last_batch_id(db_path) + 1
    batch_ids = list(range(last_batch_id, last_batch_id + amount))

    logging.info(
        f"align parameters NEXT align_guid {align_guid} batch_ids {batch_ids} name {name} guid_from {guid_from} guid_to {guid_to} total_batches {total_batches}"
    )

    lines_from = aligner.get_splitted_from(db_path)
    lines_to = aligner.get_splitted_to(db_path)

    proxy_from = aligner.get_proxy_from(db_path)
    proxy_to = aligner.get_proxy_to(db_path)

    logging.info(f"[{username}]. Cleaning images.")
    # misc.clean_img_user_foler(username, align_guid)

    # exit if batch ids is empty
    batch_ids = [x for x in batch_ids if x < total_batches][:total_batches]
    if not batch_ids:
        abort(404)

    user_db_helper.update_alignment_state_by_align_id(
        user_db_path, align_guid, con.PROC_IN_PROGRESS
    )

    # parallel processing
    logging.info(f"{username}: align started")
    res_img_best = os.path.join(
        con.STATIC_FOLDER, con.IMG_FOLDER, username, f"{align_guid}.best.png"
    )

    task_list = [
        (
            lines_from_batch,
            lines_to_batch,
            proxy_from_batch,
            proxy_to_batch,
            line_ids_from,
            line_ids_to,
            batch_id,
            batch_shift,
            window,
        )
        for lines_from_batch, lines_to_batch, proxy_from_batch, proxy_to_batch, line_ids_from, line_ids_to, batch_id in aligner.get_batch_intersected(
            lines_from,
            lines_to,
            n=config.DEFAULT_BATCHSIZE,
            window=window,
            batch_ids=batch_ids,
            batch_shift=batch_shift,
            iter3=proxy_from,
            iter4=proxy_to,
        )
    ]

    proc_count = config.PROCESSORS_COUNT

    proc = AlignmentProcessor(
        proc_count,
        db_path,
        user_db_path,
        res_img_best,
        lang_from,
        lang_to,
        align_guid,
        model_name=config.MODEL,
        embed_batch_size=config.EMBED_BATCH_SIZE,
        normalize_embeddings=config.NORMALIZE_EMBEDDINGS,
        operation=la_con.OPERATION_CALCULATE_CUSTOM,
        plot_info=config.VIS_BATCH_INFO,
        plot_regression=config.VIS_REGRESSION,
        use_proxy_from=use_proxy_from,
        use_proxy_to=use_proxy_to,
    )
    proc.add_tasks(task_list)
    proc.start_align()

    return con.EMPTY_LINES


@app.route("/items/<username>/alignment/conflicts/<align_guid>", methods=["GET"])
def get_alignment_conflicts(username, align_guid):
    """Get alignment conflicts"""
    (
        name,
        guid_from,
        guid_to,
        state,
        curr_batches,
        total_batches,
    ) = user_db_helper.get_alignment_info(username, align_guid)
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")

    if not os.path.isfile(db_path):
        abort(404)

    conflicts, rest = resolver.get_all_conflicts(
        db_path, min_chain_length=2, max_conflicts_len=20, batch_id=-1
    )
    stat1 = resolver.get_statistics(conflicts, print_stat=False)
    stat2 = resolver.get_statistics(rest, print_stat=False)
    res = [(x, stat1[x]) for x in stat1]
    res.extend([(x, stat2[x]) for x in stat2])
    res.sort(key=lambda x: x[1], reverse=True)
    return {"items": res}


@app.route(
    "/items/<username>/alignment/conflicts/<align_guid>/show/<int:id>", methods=["GET"]
)
def show_alignment_conflict(username, align_guid, id):
    """Get alignment conflict details"""
    (
        name,
        guid_from,
        guid_to,
        state,
        curr_batches,
        total_batches,
    ) = user_db_helper.get_alignment_info(username, align_guid)
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")

    if not os.path.isfile(db_path):
        abort(404)

    conflicts, rest = resolver.get_all_conflicts(
        db_path, min_chain_length=2, max_conflicts_len=20, batch_id=-1
    )
    conflicts.extend(rest)
    if not conflicts:
        return {"from": [], "to": []}
    id = id % len(conflicts)
    splitted_from, splitted_to = resolver.show_conflict(
        db_path, conflicts[id], print_conf=False
    )

    return {"from": splitted_from, "to": splitted_to}


@app.route("/items/<username>/alignment/resolve", methods=["POST"])
def resolve_conflicts(username):
    """Found and resolve conflicts in document"""
    align_guid = request.form.get("id", "")
    batch_ids = misc.parse_json_array(request.form.get("batch_ids", "[0]"))
    (
        name,
        guid_from,
        guid_to,
        state,
        curr_batches,
        total_batches,
    ) = user_db_helper.get_alignment_info(username, align_guid)
    _, lang_from = user_db_helper.get_alignment_fileinfo_from(username, guid_from)
    _, lang_to = user_db_helper.get_alignment_fileinfo_to(username, guid_to)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    use_proxy_from = True if request.form.get("use_proxy_from", "") == "true" else False
    use_proxy_to = True if request.form.get("use_proxy_to", "") == "true" else False

    print("use_proxy_from", use_proxy_from)
    print("use_proxy_to", use_proxy_to)

    # exit if batch ids is empty
    batch_ids = [x for x in batch_ids if x < total_batches][:total_batches]
    if not batch_ids:
        abort(404)

    user_db_helper.update_alignment_state_by_align_id(
        user_db_path, align_guid, con.PROC_IN_PROGRESS
    )

    res_img_best = os.path.join(
        con.STATIC_FOLDER, con.IMG_FOLDER, username, f"{align_guid}.best.png"
    )

    proc_count = config.PROCESSORS_COUNT
    proc = AlignmentProcessor(
        proc_count,
        db_path,
        user_db_path,
        res_img_best,
        lang_from,
        lang_to,
        align_guid,
        model_name=config.MODEL,
        embed_batch_size=config.EMBED_BATCH_SIZE,
        normalize_embeddings=config.NORMALIZE_EMBEDDINGS,
        mode="resolve",
        operation=la_con.OPERATION_RESOLVE,
        plot_info=config.VIS_BATCH_INFO,
        plot_regression=config.VIS_REGRESSION,
        use_proxy_from=use_proxy_from,
        use_proxy_to=use_proxy_to,
    )
    proc.add_tasks([(batch_id, total_batches) for batch_id in batch_ids])
    proc.start_resolve()

    return ("", 200)


@app.route(
    "/items/<username>/processing/<lang_from>/<lang_to>/<align_guid>/index",
    methods=["GET"],
)
def get_doc_index(username, lang_from, lang_to, align_guid):
    """Get aligned document index"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)
    index = helper.get_clear_flatten_doc_index(db_path)
    return {"items": index}


@app.route(
    "/items/<username>/processing/<lang_from>/<lang_to>/<align_guid>/<int:count>/<int:page>",
    methods=["GET"],
)
def get_processing(username, lang_from, lang_to, align_guid, count, page):
    """Get processing (aligned) document page"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)
    index = helper.get_flatten_doc_index(db_path)

    shift = (page - 1) * count
    pages = list(zip(index[shift : shift + count], range(shift, shift + count)))
    res, proxy_from_dict, proxy_to_dict = helper.get_doc_items(pages, db_path)

    lines_count = len(index)
    total_pages = (lines_count // count) + (1 if lines_count % count != 0 else 0)
    meta = {"page": page, "total_pages": total_pages}
    return {
        "items": res,
        "meta": meta,
        "proxy_from_dict": proxy_from_dict,
        "proxy_to_dict": proxy_to_dict,
    }


@app.route(
    "/items/<username>/processing/<lang_from>/<lang_to>/<align_guid>", methods=["POST"]
)
def get_processing_by_ids(username, lang_from, lang_to, align_guid):
    """Get processing (aligned) items by ids"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)

    index = helper.get_flatten_doc_index(db_path)
    index_ids = misc.parse_json_array(request.form.get("index_ids", "[]"))

    index_items = [(index[i], i) for i in index_ids]
    res = {}
    data, proxy_from_dict, proxy_to_dict = helper.get_doc_items(index_items, db_path)

    for i, item in zip(index_ids, data):
        res[i] = item

    return {
        "items": res,
        "proxy_from_dict": proxy_from_dict,
        "proxy_to_dict": proxy_to_dict,
    }


@app.route(
    "/items/<username>/processing/<lang_from>/<lang_to>/<align_guid>/meta",
    methods=["GET"],
)
def get_processing_metadata(username, lang_from, lang_to, align_guid):
    """Get processing (aligned) document metadata"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)

    batch_ids = [x[0] for x in user_db_helper.get_processed_batch_ids(db_path)]
    meta = {"batch_ids": batch_ids, "align_guid": align_guid}

    return {"meta": meta}


@app.route(
    "/items/<username>/splitted/from/<lang_from>/<lang_to>/<align_guid>",
    methods=["POST"],
)
def get_splitted_from_by_ids(username, lang_from, lang_to, align_guid):
    """Get splitted from lines by array of IDs"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)
    text_ids = misc.parse_json_array(request.form.get("ids", "[]"))

    res = {}
    if text_ids:
        for (
            id,
            text,
            proxy,
            exclude,
            _,
            h1,
            h2,
            h3,
            h4,
            h5,
            divider,
        ) in helper.get_splitted_from_by_id(db_path, text_ids):
            res[id] = {"t": text, "p": proxy if proxy else "", "e": exclude == 1}
    return {"items": res}


@app.route(
    "/items/<username>/splitted/to/<lang_from>/<lang_to>/<align_guid>", methods=["POST"]
)
def get_splitted_to_by_ids(username, lang_from, lang_to, align_guid):
    """Get splitted to lines by array of IDs"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)
    text_ids = misc.parse_json_array(request.form.get("ids", "[]"))

    res = {}
    if text_ids:
        for (
            id,
            text,
            proxy,
            exclude,
            _,
            h1,
            h2,
            h3,
            h4,
            h5,
            divider,
        ) in helper.get_splitted_to_by_id(db_path, text_ids):
            res[id] = {"t": text, "p": proxy if proxy else "", "e": exclude == 1}

    return {"items": res}


@app.route(
    "/items/<username>/processing/<lang_from>/<lang_to>/<align_guid>/candidates/<text_type>/<int:index_id>/<int:count_before>/<int:count_after>",
    methods=["GET"],
)
def get_processing_candidates(
    username,
    lang_from,
    lang_to,
    align_guid,
    text_type,
    index_id,
    count_before,
    count_after,
):
    """Get splitted lines by some interval"""
    if text_type not in (con.TYPE_FROM, con.TYPE_TO):
        abort(404)
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)

    index = helper.get_clear_flatten_doc_index(db_path)
    if index_id < 0 or index_id >= len(index):
        return

    direction = 3 if text_type == con.TYPE_TO else 1
    if index_id > 0:
        line_ids = misc.parse_json_array(index[index_id - 1][direction])
    else:
        line_ids = misc.parse_json_array(index[index_id][direction])

    while index_id > 0:
        print("line_ids", line_ids)
        if not line_ids:
            index_id -= 1
            line_ids = misc.parse_json_array(index[index_id][direction])
        else:
            break

    if not line_ids or index_id == 0:
        line_id = 1
    else:
        line_id = line_ids[0]

    id_from = line_id - count_before
    id_to = line_id + count_after

    candidates = editor_helper.get_candidates_page(db_path, text_type, id_from, id_to)

    return {"items": candidates}


@app.route(
    "/items/<username>/processing/<lang_from>/<lang_to>/<align_guid>/edit",
    methods=["POST"],
)
def edit_processing(username, lang_from, lang_to, align_guid):
    """Edit processing document"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)

    index_id, index_id_is_int = misc.try_parse_int(request.form.get("index_id", -1))
    text = request.form.get("text", "")
    text_type = request.form.get("text_type", con.TYPE_TO)
    operation = request.form.get("operation", "")
    target = request.form.get("target", "")
    candidate_line_id, _ = misc.try_parse_int(request.form.get("candidate_line_id", -1))
    candidate_text = request.form.get("candidate_text", "")
    batch_id, _ = misc.try_parse_int(request.form.get("batch_id", -1))
    batch_index_id, _ = misc.try_parse_int(request.form.get("batch_index_id", -1))

    # print("OPERATION:", operation, "text_type:", text_type)

    if index_id_is_int:
        editor.edit_doc(
            db_path,
            index_id,
            text,
            operation,
            target,
            candidate_line_id,
            candidate_text,
            batch_id,
            batch_index_id,
            text_type,
        )
    else:
        abort(400)
    return ("", 200)


@app.route(
    "/items/<username>/splitted/<lang_from>/<lang_to>/<align_guid>/download/<lang>/<direction>",
    methods=["GET"],
)
def download_splitted_from_db(
    username, lang_from, lang_to, align_guid, lang, direction
):
    """Download splitted document file"""
    logging.info(
        f"[{username}]. Downloading {lang} ({direction} side) align_guid:{align_guid} splitted document."
    )
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    download_folder = os.path.join(con.UPLOAD_FOLDER, username, con.DOWNLOAD_FOLDER)
    misc.check_folder(download_folder)
    download_file = os.path.join(
        download_folder,
        "{0}_{1}_{2}_{3}.txt".format(align_guid, lang, direction, timestamp),
    )

    if direction == "from":
        lines = aligner.get_splitted_from(db_path)
    else:
        lines = aligner.get_splitted_to(db_path)

    with open(download_file, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))

    logging.info(f"[{username}]. Document found. Path: {download_file}. Sent to user.")
    return send_file(download_file)


@app.route(
    "/items/<username>/processing/<lang_from>/<lang_to>/<align_guid>/download/<lang>/<side>/<file_format>",
    methods=["POST"],
)
def download_processsing(
    username, lang_from, lang_to, align_guid, lang, side, file_format
):
    """Download processsing document"""
    logging.info(
        f"[{username}]. Downloading {lang_from}-{lang_to} {align_guid} {lang} {side} result document."
    )
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    if not os.path.isfile(db_path):
        abort(404)

    paragraphs = request.form.get("paragraphs", False)
    pars_direction = request.form.get("direction", "to")
    left_side = request.form.get("left_lang", con.TYPE_FROM)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    download_folder = os.path.join(con.UPLOAD_FOLDER, username, con.DOWNLOAD_FOLDER)
    misc.check_folder(download_folder)
    download_file = os.path.join(
        download_folder,
        "{0}_{1}_{2}_{3}.{4}".format(align_guid, lang, side, timestamp, file_format),
    )

    logging.debug(f"[{username}]. Preparing file for downloading {download_file}.")

    if not side:
        side = "from"

    if paragraphs == "true":
        try:
            paragraphs, _, _, _ = reader.get_paragraphs(db_path, pars_direction)
            saver.save_paragraphs(paragraphs, side, download_file)
            return send_file(download_file, as_attachment=True)
        except:
            return abort(404)

    if left_side == "from":
        lang_order = [con.TYPE_FROM, con.TYPE_TO]
    else:
        lang_order = [con.TYPE_TO, con.TYPE_FROM]

    if file_format == con.FORMAT_TMX:
        saver.save_tmx(db_path, download_file, lang_from, lang_to)
    if file_format == con.FORMAT_XML:
        saver.save_xml(db_path, download_file, lang_order, pars_direction)
    if file_format == con.FORMAT_JSON:
        saver.save_json(db_path, download_file, lang_order, pars_direction)
    elif file_format == con.FORMAT_PLAIN:
        saver.save_plain_text(db_path, download_file, side)

    logging.debug(f"[{username}]. File {download_file} prepared. Sent to user.")
    return send_file(download_file, as_attachment=True)


@app.route("/items/<username>/processing/list/<lang_from>/<lang_to>", methods=["GET"])
def list_processing(username, lang_from, lang_to):
    """Get processing documents list"""
    logging.debug(
        f"[{username}]. Processing list. Language code lang_from: {lang_from}. Language code lang_to: {lang_to}."
    )
    if not lang_from or not lang_to:
        logging.warning(f"[{username}]. Wrong language code: {lang_from}-{lang_to}.")
        return con.EMPTY_FILES
    processing_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.PROCESSING_FOLDER, lang_from, lang_to
    )
    misc.check_folder(processing_folder)
    files = {
        "items": {
            lang_from: misc.get_processing_list_with_state(username, lang_from, lang_to)
        }
    }
    return files


@app.route(
    "/items/<username>/align/stop/<lang_from>/<lang_to>/<align_guid>", methods=["POST"]
)
def stop_alignment(username, lang_from, lang_to, align_guid):
    """Stop alignment process"""
    logging.info(f"[{username}]. Stopping alignment for {lang_from}-{lang_to}.")
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    user_db_helper.update_alignment_state_by_align_id(
        user_db_path, align_guid, con.PROC_IN_PROGRESS_DONE
    )
    return ("", 200)


@app.route(
    "/items/<username>/create/<lang_from>/<lang_to>/<align_guid>/preview",
    methods=["POST"],
)
def get_book_preview(username, lang_from, lang_to, align_guid):
    """Get the beginning of the book"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    direction = request.form.get("par_direction", con.TYPE_TO)
    left_side = request.form.get("left_lang", con.TYPE_FROM)
    style = request.form.get("style", "none")

    if not os.path.isfile(db_path):
        abort(404)

    if reader.is_empty_cells(db_path):
        abort(400)

    par_amount = 5

    paragraphs, delimeters, metas, _ = reader.get_paragraphs(
        db_path=db_path, direction=direction, par_amount=par_amount
    )

    if left_side == "from":
        lang_order = [con.TYPE_FROM, con.TYPE_TO]
    else:
        lang_order = [con.TYPE_TO, con.TYPE_FROM]

    res_html = reader.create_polybook_preview(
        lang_ordered=lang_order,
        paragraphs=paragraphs,
        delimeters=delimeters,
        metas=metas,
        template=style,
        styles=[],
        par_amount=par_amount,
    )

    return {"items": res_html}


@app.route(
    "/items/<username>/create/<lang_from>/<lang_to>/<align_guid>/download",
    methods=["POST"],
)
def download_book(username, lang_from, lang_to, align_guid):
    """Get the beginning of the book"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{align_guid}.db")
    direction = request.form.get("par_direction", con.TYPE_TO)
    left_side = request.form.get("left_lang", con.TYPE_FROM)
    style = request.form.get("style", "none")

    if not os.path.isfile(db_path):
        abort(404)

    if reader.is_empty_cells(db_path):
        abort(400)

    paragraphs, delimeters, metas, sent_counter = reader.get_paragraphs(
        db_path, direction
    )

    if left_side == "from":
        lang_order = [con.TYPE_FROM, con.TYPE_TO]
    else:
        lang_order = [con.TYPE_TO, con.TYPE_FROM]

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    download_folder = os.path.join(con.UPLOAD_FOLDER, username, con.DOWNLOAD_FOLDER)
    misc.check_folder(download_folder)
    download_file = os.path.join(
        download_folder,
        "{0}_{1}_{2}_{3}.html".format(align_guid, lang_from, lang_from, timestamp),
    )

    reader.create_book(
        lang_ordered=lang_order,
        paragraphs=paragraphs,
        delimeters=delimeters,
        metas=metas,
        sent_counter=sent_counter,
        output_path=download_file,
        template=style,
        styles=[],
    )

    logging.debug(f"[{username}]. File (book) {download_file} prepared. Sent to user.")
    return send_file(download_file, as_attachment=True)


@app.route(
    "/items/<username>/edit/find/<lang_from>/<lang_to>/<aling_id>/<lang>/<int:line_id>",
    methods=["GET"],
)
def get_line_id_position(username, lang_from, lang_to, aling_id, lang, line_id):
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{aling_id}.db")

    if not os.path.isfile(db_path):
        abort(404)

    direction = "from" if lang == lang_from else "to"
    res = editor_helper.get_line_id_index_position(db_path, line_id, direction)

    return {"pos": res}


@app.route(
    "/items/<username>/edit/exclude/<lang_from>/<lang_to>/<aling_id>", methods=["POST"]
)
def switch_excluded(username, lang_from, lang_to, aling_id):
    """Switch excluded flag for unused string"""
    db_folder = os.path.join(
        con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to
    )
    db_path = os.path.join(db_folder, f"{aling_id}.db")

    line_id = request.form.get("line_id", -1)
    text_type = request.form.get("text_type", con.TYPE_FROM)

    if text_type == "from":
        editor_helper.switch_excluded_splitted_from(db_path, line_id)
    else:
        editor_helper.switch_excluded_splitted_to(db_path, line_id)
    return ("", 200)


@app.route("/items/contents", methods=["GET"])
def show_contents():
    """Return alignments list across all users"""
    contents = main_db_helper.get_contents()
    return {"items": contents}


@app.route("/debug/items", methods=["GET"])
def show_items_tree():
    """Show all files in data folder"""
    tree_path = os.path.join(tempfile.gettempdir(), "items_tree.txt")
    logging.debug(f"Temp file for tree structure: {tree_path}.")
    with open(tree_path, mode="w", encoding="utf-8") as tree_out:
        for root, dirs, files in os.walk(con.UPLOAD_FOLDER):
            level = root.replace(con.UPLOAD_FOLDER, "").count(os.sep)
            indent = " " * 4 * (level)
            tree_out.write(f"{indent}{os.path.basename(root)}" + "\n")
            subindent = " " * 4 * (level + 1)
            for file in files:
                tree_out.write(f"{subindent}{file}" + "\n")
    return send_file(tree_path)


@app.route("/debug/text/<username>/<lang>/<int:index>", methods=["GET"])
def show_file(username, lang, index):
    """Show text file"""
    files_dir = os.path.join(con.UPLOAD_FOLDER, username, con.SPLITTED_FOLDER, lang)
    files = os.listdir(files_dir)

    if not files or len(files) < index + 1:
        return ("", 200)

    # delete
    print(os.path.join(files_dir, files[index]))

    return send_file(os.path.join(files_dir, files[index]))


# Not API calls treated like static queries
@app.route("/<path:path>")
def route_frontend(path):
    """Route static requests"""
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, "index.html")
        return send_file(index_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=config.API_PORT)
