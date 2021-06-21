import logging
import os
import pathlib
import sqlite3

import constants as con


def init_main_db():
    """Init main database"""
    pathlib.Path(os.path.join(con.UPLOAD_FOLDER)
                 ).mkdir(parents=True, exist_ok=True)
    main_db_path = os.path.join(con.UPLOAD_FOLDER, con.MAIN_DB_NAME)
    if not os.path.isfile(main_db_path):
        logging.info(f"creating main db: {main_db_path}")
        with sqlite3.connect(main_db_path) as db:
            db.execute(
                'create table global_alignments(id integer primary key, username text, lang_from text, lang_to text, guid text, name varchar, state integer, insert_ts text, deleted integer)')


def get_contents():
    """Get alignments list from main database"""
    main_db_path = os.path.join(con.UPLOAD_FOLDER, con.MAIN_DB_NAME)
    with sqlite3.connect(main_db_path) as db:
        res = db.execute(
            f'select g.username, g.lang_from, g.lang_to, g.guid, g.name, g.insert_ts from global_alignments g where g.deleted <> 1 order by g.username').fetchall()
    return res
