import datetime
import logging
import os
import pathlib
import sqlite3
import uuid

import constants as con


def get_batches_count(db_path, align_guid):
    """Get amount of already processed batches"""
    with sqlite3.connect(db_path) as db:
        count = db.execute("select count(*) from alignment_progress where guid=:guid", {"guid": align_guid}).fetchone()
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
        user_db.execute('update alignments set state=:state, curr_batches=:curr_batches where guid=:guid', {
            "guid": align_guid, "state": state, "curr_batches": batches_count})


def update_alignment_state(user_db_path, align_guid, state, curr_batches=None, total_batches=None):
    """Update alignment state"""
    with sqlite3.connect(user_db_path) as db:
        if curr_batches and curr_batches >= 0 and total_batches:
            logging.info(
                f"updating alignment state total_batches {total_batches} curr_batches {curr_batches} state {state}")
            db.execute('update alignments set state=:state, curr_batches=:curr_batches, total_batches=:total_batches where guid=:guid', {
                "guid": align_guid, "state": state, "curr_batches": curr_batches, "total_batches": total_batches})
        else:
            db.execute('update alignments set state=:state where guid=:guid', {
                "guid": align_guid, "state": state})


def update_alignment_state_by_align_id(user_db_path, align_id, state):
    """Update alignment state"""
    with sqlite3.connect(user_db_path) as db:
        db.execute('update alignments set state=:state where guid=:guid', {
            "guid": align_id, "state": state})


def init_user_db(username):
    """Init user database with tables structure"""
    pathlib.Path(os.path.join(con.UPLOAD_FOLDER, username)
                 ).mkdir(parents=True, exist_ok=True)
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    if not os.path.isfile(db_path):
        logging.info(f"creating user db: {db_path}")
        with sqlite3.connect(db_path) as db:
            db.execute(
                'create table documents(id integer primary key, guid text, lang text, name text)')
            db.execute(
                'create table alignments(id integer primary key, guid text, guid_from text, guid_to text, lang_from text, lang_to text, name text, state integer, curr_batches integer, total_batches integer, deleted integer default 0 NOT NULL)')
            db.execute(
                'create table version(id integer primary key, version text)')
            #tracking the alignment progress
            db.execute(
                'create table alignment_progress(id integer primary key, guid text, batch_id int, UNIQUE(guid, batch_id) ON CONFLICT IGNORE)')
            db.execute('insert into version(version) values (?)', (con.USER_DB_VERSION,))


def update_alignment_progress(db, align_guid, batch_id):
    """Update batch IDs in order to detect current alignment progress on UI"""
    db.execute(
        "insert or ignore into alignment_progress(guid, batch_id) values (?, ?)", (align_guid, batch_id))


def alignment_exists(username, guid_from, guid_to):
    """Check if alignment already exists"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        cur = db.execute("select * from alignments where guid_from=:guid_from and guid_to=:guid_to and deleted <> 1", {
                         "guid_from": guid_from, "guid_to": guid_to})
        return bool(cur.fetchone())


def alignment_guid_exists(username, guid):
    """Check if alignment already exists by alignment guid"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        cur = db.execute(
            "select * from alignments where guid=:guid", {"guid": guid})
        return bool(cur.fetchone())


def register_alignment(username, lang_from, lang_to, guid, guid_from, guid_to, name, total_batches):
    """Register new alignment in user.db and main.db"""
    main_db_path = os.path.join(con.UPLOAD_FOLDER, con.MAIN_DB_NAME)
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    if not alignment_exists(username,  guid_from, guid_to):
        with sqlite3.connect(main_db_path) as main_db:
            main_db.execute('insert into global_alignments(guid, username, lang_from, lang_to, name, state, insert_ts, deleted) values (:guid, :username, :lang_from, :lang_to, :name, 2, :insert_ts, 0) ', {
                "guid": guid, "username": username, "lang_from": lang_from, "lang_to": lang_to, "name": name, "insert_ts": datetime.datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')})
        with sqlite3.connect(user_db_path) as db:
            db.execute('insert into alignments(guid, guid_from, guid_to, lang_from, lang_to, name, state, curr_batches, total_batches) values (:guid, :guid_from, :guid_to, :lang_from, :lang_to, :name, 2, 0, :total_batches) ', {
                       "guid": guid, "guid_from": guid_from, "guid_to": guid_to, "lang_from": lang_from, "lang_to": lang_to, "name": name, "total_batches": total_batches})
    return


def get_alignment_id(username, guid_from, guid_to):
    """Return alignment id"""
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(user_db_path) as db:
        res = db.execute("select guid from alignments where guid_from=:guid_from and guid_to=:guid_to", {
                         "guid_from": guid_from, "guid_to": guid_to}).fetchone()
        return res[0] if res else None


def delete_alignment(username, guid):
    """Mark alignment as deleted"""
    main_db_path = os.path.join(con.UPLOAD_FOLDER, con.MAIN_DB_NAME)
    user_db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(main_db_path) as db:
        db.execute('update global_alignments set deleted = 1 where guid=:guid', {
                   "guid": guid})
    with sqlite3.connect(user_db_path) as db:
        db.execute('update alignments set deleted = 1 where guid=:guid', {
                   "guid": guid})


def file_exists(username, lang, name):
    """Check if file already exists"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        cur = db.execute("select * from documents where lang=:lang and name=:name", {
                         "lang": lang, "name": name})
        return bool(cur.fetchone())


def file_exists_by_guid(username, guid):
    """Check if file already exists by guid"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        cur = db.execute(
            "select * from documents where guid=:guid", {"guid": guid})
        return bool(cur.fetchone())


def register_file(username, lang, name):
    """Register new file in database"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    guid = uuid.uuid4().hex
    with sqlite3.connect(db_path) as db:
        db.execute('insert into documents(guid, lang, name) values (:guid, :lang, :name) ', {
            "guid": guid, "lang": lang, "name": name})


def delete_document(username, guid, lang, filename):
    """Delete uploaded document and clean database"""
    raw_path = os.path.join(con.UPLOAD_FOLDER, username,
                            con.RAW_FOLDER, lang, filename)
    proxy_path = os.path.join(
        con.UPLOAD_FOLDER, username, con.PROXY_FOLDER, lang, filename)

    if os.path.isfile(raw_path):
        os.remove(raw_path)
    if os.path.isfile(proxy_path):
        os.remove(proxy_path)

    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        db.execute('delete from documents where guid=:guid', {"guid": guid})


def get_documents_list(username, lang=None):
    """Get documents list by language code"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        if not lang:
            return db.execute("select name, guid, lang from documents").fetchall()
        else:
            return db.execute("select name, guid, lang from documents where lang=:lang", {
                "lang": lang}).fetchall()


def get_document_info(username, guid):
    """Get documents list by language code"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute("select name, lang from documents where guid=:guid", {
            "guid": guid}).fetchone()
    return ([res[0], res[1]]) if res else None


def get_alignment_fileinfo_from(username, guid):
    """Get file (from) info by id from alignments table"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute("select guid_from, lang_from from alignments where guid_from=:guid", {
            "guid": guid}).fetchone()
    return ([res[0], res[1]]) if res else None


def get_alignment_fileinfo_to(username, guid):
    """Get file (to) info by id from alignments table"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute("select guid_to, lang_to from alignments where guid_to=:guid", {
            "guid": guid}).fetchone()
    return ([res[0], res[1]]) if res else None


def get_alignment_info(username, guid):
    """Get alignment info by id"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        return db.execute("select name, guid_from, guid_to, state, curr_batches, total_batches from alignments where guid=:guid", {"guid": guid}).fetchone()


def get_alignment_progress(user_db_path, align_guid):
    """Get alignment progress info"""
    with sqlite3.connect(user_db_path) as db:
        return db.execute("select curr_batches, total_batches from alignments where guid=:guid", {"guid": align_guid}).fetchone()


def get_alignments_list(username, lang_from, lang_to):
    """Get alignments list by language code"""
    db_path = os.path.join(con.UPLOAD_FOLDER, username, con.USER_DB_NAME)
    with sqlite3.connect(db_path) as db:
        res = db.execute("""select
                                a.guid, a.name, a.guid_from, a.guid_to, a.state, a.curr_batches, a.total_batches
                            from alignments a
                            where
                                a.lang_from=:lang_from and a.lang_to=:lang_to
                                and a.deleted <> 1""", {
                         "lang_from": lang_from, "lang_to": lang_to}).fetchall()
        return res
