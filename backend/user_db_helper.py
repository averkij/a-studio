import datetime
import logging
import os
import pathlib
import sqlite3
import uuid
import shutil
from lingtrain_aligner import helper as aligner_helper
from lingtrain_aligner import vis_helper, splitter
import misc
import config

import constants as con


def get_batches_count(db_path, align_guid):
    """Get amount of already processed batches"""
    with sqlite3.connect(db_path) as db:
        count = db.execute(
            "select count(*) from alignment_progress where guid=:guid",
            {"guid": align_guid},
        ).fetchone()
    return count[0]


def get_last_batch_id(db_path):
    """Get amount of already processed batches"""
    with sqlite3.connect(db_path) as db:
        batch_ids = db.execute("select batch_id from batches").fetchall()
    res = [x[0] for x in batch_ids]
    if not res:
        return -1
    return max(res)


def get_processed_batch_ids(db_path):
    """Get IDs of the processed batches"""
    with sqlite3.connect(db_path) as db:
        res = db.execute("select batch_id from batches").fetchall()
    return res


def increment_alignment_state(user_db_path, align_guid, state):
    """Increment alignment progress"""
    batches_count = get_batches_count(user_db_path, align_guid)
    with sqlite3.connect(user_db_path) as user_db:
        print("batches_count", batches_count)
        user_db.execute(
            "update alignments set state=:state, curr_batches=:curr_batches where guid=:guid",
            {"guid": align_guid, "state": state, "curr_batches": batches_count},
        )


def update_alignment_state(
    user_db_path, align_guid, state, curr_batches=None, total_batches=None
):
    """Update alignment state"""
    with sqlite3.connect(user_db_path) as db:
        if curr_batches and curr_batches >= 0 and total_batches:
            logging.info(
                f"updating alignment state total_batches {total_batches} curr_batches {curr_batches} state {state}"
            )
            db.execute(
                "update alignments set state=:state, curr_batches=:curr_batches, total_batches=:total_batches where guid=:guid",
                {
                    "guid": align_guid,
                    "state": state,
                    "curr_batches": curr_batches,
                    "total_batches": total_batches,
                },
            )
        else:
            db.execute(
                "update alignments set state=:state where guid=:guid",
                {"guid": align_guid, "state": state},
            )


def update_alignment_state_by_align_id(user_db_path, align_id, state):
    """Update alignment state"""
    with sqlite3.connect(user_db_path) as db:
        db.execute(
            "update alignments set state=:state where guid=:guid",
            {"guid": align_id, "state": state},
        )


def update_alignment_proxy_loaded(username, align_id, direction):
    """Update alignment proxy_loaded"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        if direction == "from":
            db.execute(
                "update alignments set proxy_from_loaded=1 where guid=:guid",
                {"guid": align_id},
            )
        else:
            db.execute(
                "update alignments set proxy_to_loaded=1 where guid=:guid",
                {"guid": align_id},
            )


def init_user_db(username):
    """Init user database with tables structure"""
    pathlib.Path(os.path.join(con.UPLOAD_FOLDER, username)).mkdir(
        parents=True, exist_ok=True
    )
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    if not os.path.isfile(db_path):
        logging.info(f"creating user db: {db_path}")
        with sqlite3.connect(db_path) as db:
            db.execute(
                "create table documents(id integer primary key, guid text, lang text, name text)"
            )
            db.execute(
                "create table alignments(id integer primary key, guid text, guid_from text, guid_to text, lang_from text, lang_to text, \
                    name text, state integer, curr_batches integer, total_batches integer, deleted integer default 0 NOT NULL, \
                    proxy_from_loaded integer default 0 NOT NULL, proxy_to_loaded integer default 0 NOT NULL, uploaded default 0)"
            )
            db.execute("create table version(id integer primary key, version text)")
            # tracking the alignment progress
            db.execute(
                "create table alignment_progress(id integer primary key, guid text, batch_id int, UNIQUE(guid, batch_id) ON CONFLICT IGNORE)"
            )
            db.execute(
                "insert into version(version) values (?)", (con.USER_DB_VERSION,)
            )


def update_alignment_progress(db_path, align_guid, batch_id):
    """Update batch IDs in order to detect current alignment progress on UI"""
    with sqlite3.connect(db_path) as db:
        db.execute(
            "insert or ignore into alignment_progress(guid, batch_id) values (?, ?)",
            (align_guid, batch_id),
        )


def alignment_exists(username, guid_from, guid_to):
    """Check if alignment already exists"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        cur = db.execute(
            "select * from alignments where guid_from=:guid_from and guid_to=:guid_to and deleted <> 1",
            {"guid_from": guid_from, "guid_to": guid_to},
        )
        return bool(cur.fetchone())


def alignment_guid_exists(username, guid):
    """Check if alignment already exists by alignment guid"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        cur = db.execute("select * from alignments where guid=:guid", {"guid": guid})
        return bool(cur.fetchone())


def register_alignment(
    username,
    lang_from,
    lang_to,
    guid,
    guid_from,
    guid_to,
    name,
    total_batches,
    force=False,
):
    """Register new alignment in user.db and main.db"""
    main_db_path = os.path.join(con.UPLOAD_FOLDER, con.MAIN_DB_NAME)
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    if not alignment_exists(username, guid_from, guid_to) or force:
        with sqlite3.connect(main_db_path) as main_db:
            main_db.execute(
                "insert into global_alignments(guid, username, lang_from, lang_to, name, state, insert_ts, deleted) values (:guid, :username, :lang_from, :lang_to, :name, 2, :insert_ts, 0) ",
                {
                    "guid": guid,
                    "username": username,
                    "lang_from": lang_from,
                    "lang_to": lang_to,
                    "name": name,
                    "insert_ts": datetime.datetime.utcnow().strftime(
                        "%Y-%m-%d_%H:%M:%S"
                    ),
                },
            )
        with sqlite3.connect(user_db_path) as db:
            db.execute(
                "insert into alignments(guid, guid_from, guid_to, lang_from, lang_to, name, state, curr_batches, total_batches) values (:guid, :guid_from, :guid_to, :lang_from, :lang_to, :name, 2, 0, :total_batches) ",
                {
                    "guid": guid,
                    "guid_from": guid_from,
                    "guid_to": guid_to,
                    "lang_from": lang_from,
                    "lang_to": lang_to,
                    "name": name,
                    "total_batches": total_batches,
                },
            )
    return


def get_alignment_id(username, guid_from, guid_to):
    """Return alignment id"""
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(user_db_path) as db:
        res = db.execute(
            "select guid from alignments where guid_from=:guid_from and guid_to=:guid_to",
            {"guid_from": guid_from, "guid_to": guid_to},
        ).fetchone()
        return res[0] if res else None


def delete_alignment(username, guid):
    """Mark alignment as deleted"""
    main_db_path = os.path.join(con.UPLOAD_FOLDER, con.MAIN_DB_NAME)
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(main_db_path) as db:
        db.execute(
            "update global_alignments set deleted = 1 where guid=:guid", {"guid": guid}
        )
    with sqlite3.connect(user_db_path) as db:
        db.execute("update alignments set deleted = 1 where guid=:guid", {"guid": guid})


def file_exists(username, lang, name):
    """Check if file already exists"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        cur = db.execute(
            "select * from documents where lang=:lang and name=:name",
            {"lang": lang, "name": name},
        )
        return bool(cur.fetchone())


def file_exists_by_guid(username, guid):
    """Check if file already exists by guid"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        cur = db.execute("select * from documents where guid=:guid", {"guid": guid})
        return bool(cur.fetchone())


def register_file(username, lang, name, guid=None):
    """Register new file in database"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    if not guid:
        guid = uuid.uuid4().hex
    with sqlite3.connect(db_path) as db:
        db.execute(
            "insert into documents(guid, lang, name) values (:guid, :lang, :name) ",
            {"guid": guid, "lang": lang, "name": name},
        )


def delete_document(username, guid, lang, filename):
    """Delete uploaded document and clean database"""
    raw_path = os.path.join(con.UPLOAD_FOLDER, username, con.RAW_FOLDER, lang, filename)
    proxy_path = os.path.join(
        con.UPLOAD_FOLDER, username, con.PROXY_FOLDER, lang, filename
    )

    if os.path.isfile(raw_path):
        os.remove(raw_path)
    if os.path.isfile(proxy_path):
        os.remove(proxy_path)

    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        db.execute("delete from documents where guid=:guid", {"guid": guid})


def get_documents_list(username, lang=None):
    """Get documents list by language code"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        if not lang:
            return db.execute("select name, guid, lang from documents").fetchall()
        else:
            return db.execute(
                "select name, guid, lang from documents where lang=:lang",
                {"lang": lang},
            ).fetchall()


def get_document_info(username, guid):
    """Get documents list by language code"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute(
            "select name, lang from documents where guid=:guid", {"guid": guid}
        ).fetchone()
    return ([res[0], res[1]]) if res else None


def get_alignment_fileinfo_from(username, guid):
    """Get file (from) info by id from alignments table"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute(
            "select guid_from, lang_from from alignments where guid_from=:guid",
            {"guid": guid},
        ).fetchone()
    return ([res[0], res[1]]) if res else None


def get_alignment_fileinfo_to(username, guid):
    """Get file (to) info by id from alignments table"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute(
            "select guid_to, lang_to from alignments where guid_to=:guid",
            {"guid": guid},
        ).fetchone()
    return ([res[0], res[1]]) if res else None


def get_alignment_info(username, guid):
    """Get alignment info by id"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute(
            "select name, guid_from, guid_to, state, curr_batches, total_batches, lang_from, lang_to, uploaded from alignments where guid=:guid",
            {"guid": guid},
        ).fetchone()
        return res


def get_alignment_progress(user_db_path, align_guid):
    """Get alignment progress info"""
    with sqlite3.connect(user_db_path) as db:
        return db.execute(
            "select curr_batches, total_batches from alignments where guid=:guid",
            {"guid": align_guid},
        ).fetchone()


def get_alignments_list(username, lang_from, lang_to):
    """Get alignments list by language code"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute(
            """select
                                a.guid, a.name, a.guid_from, a.guid_to, a.state, a.curr_batches, a.total_batches, a.proxy_from_loaded, a.proxy_to_loaded
                            from alignments a
                            where
                                a.lang_from=:lang_from and a.lang_to=:lang_to
                                and a.deleted <> 1""",
            {"lang_from": lang_from, "lang_to": lang_to},
        ).fetchall()
        return res


def get_version(db_path):
    """Get user database version"""
    with sqlite3.connect(db_path) as db:
        res = db.execute(f"select v.version from version v").fetchone()
    return float(res[0])


def set_alignment_uploaded(username, align_guid):
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        db.execute(
            "update alignments set uploaded=1 where guid=:guid",
            {"guid": align_guid},
        )


def process_uploaded_alignment(align_db_path, username):
    """Check and register alignment database from Lingtrain file"""
    try:
        alignment_version = aligner_helper.get_version(align_db_path)  # 6.2+

        user_db_version = get_version(align_db_path)  # 5.1+
        user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)

        db_name = os.path.basename(align_db_path)
        align_guid = db_name.split(".")[0]
        lang_from, lang_to = aligner_helper.get_lang_codes(align_db_path)

        if not splitter.is_lang_code_valid(lang_from):
            lang_from = splitter.XX_CODE
        if not splitter.is_lang_code_valid(lang_to):
            lang_to = splitter.XX_CODE

        if alignment_version <= 6.2:
            name_from, name_to, guid_from, guid_to = (
                f"from_{lang_from}",
                f"to_{lang_to}",
                "no_guid",
                "no_guid",
            )
            alignment_name = f"[{name_from}]-[{name_to}]"
        else:
            name_from, name_to, guid_from, guid_to = aligner_helper.get_files_info(
                align_db_path
            )
            alignment_name = aligner_helper.get_name(align_db_path)

        batches_info = aligner_helper.get_batches_info(align_db_path)
        batch_ids = [x[0] for x in batches_info]

        batch_size = config.DEFAULT_BATCHSIZE
        len_from, _ = misc.get_texts_length(align_db_path)
        is_last = len_from % batch_size > 0
        total_batches = (
            len_from // batch_size + 1 if is_last else len_from // batch_size
        )
        curr_batches = len(batch_ids)

        # alignments table and main_db
        register_alignment(
            username,
            lang_from,
            lang_to,
            align_guid,
            guid_from,
            guid_to,
            f"Uploaded: {alignment_name}",
            total_batches=total_batches,
            force=True,
        )

        # alignment_progress table
        for batch_id in batch_ids:
            update_alignment_progress(user_db_path, align_guid, batch_id)

        # alignments table
        if curr_batches == total_batches:
            state = con.PROC_DONE
        else:
            state = con.PROC_IN_PROGRESS_DONE
        increment_alignment_state(user_db_path, align_guid, state)

        # documents table
        # register_file(username, lang_from, name_from, guid_from)
        # register_file(username, lang_to, name_to, guid_to)

        # move alignment
        new_path = os.path.join(
            con.UPLOAD_FOLDER, username, con.DB_FOLDER, lang_from, lang_to, db_name
        )
        misc.check_folder(os.path.dirname(new_path))

        if user_db_version >= 5.1:
            set_alignment_uploaded(username, align_guid)

        print("moving to", new_path)
        shutil.copyfile(align_db_path, new_path)
        # shutil.move(align_db_path, new_path)

        # recalculate images
        img_path = os.path.join(
            con.STATIC_FOLDER, con.IMG_FOLDER, username, f"{align_guid}.best.png"
        )
        for batch_id, _, _, _ in batches_info:
            vis_helper.visualize_alignment_by_db(
                new_path,
                img_path,
                lang_name_from=lang_from,
                lang_name_to=lang_to,
                batch_ids=[batch_id],
                transparent_bg=True,
                show_info=config.VIS_BATCH_INFO,
                show_regression=config.VIS_REGRESSION,
            )

    except Exception as e:
        error_text = f"Error while reading uploaded alignment: {str(e)}"
        print(error_text)
        return (error_text, 400)

    langs = {"items": [lang_from, lang_to]}

    return langs
