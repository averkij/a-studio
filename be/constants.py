"""App constants"""

UPLOAD_FOLDER = "data"
STATIC_FOLDER = "static"
RAW_FOLDER = "raw"
PROXY_FOLDER = "proxy"
SPLITTED_FOLDER = "splitted"
NGRAM_FOLDER = "ngramed"
PROCESSING_FOLDER = "processing"
DOWNLOAD_FOLDER = "download"
DONE_FOLDER = "done"
DB_FOLDER = "db"
IMG_FOLDER = "img"
FORMAT_PLAIN = "txt"
FORMAT_TMX = "tmx"
TYPE_FROM = "from"
TYPE_TO = "to"

USER_DB_NAME = "user.db"
MAIN_DB_NAME = "main.db"

PROC_INIT = 0
PROC_IN_PROGRESS = 1
PROC_IN_PROGRESS_DONE = 2
PROC_DONE = 3
PROC_ERROR = 4

EMPTY_LINES = {"items": {"ru": [], "zh": []}}
EMPTY_SIMS = {"items": {"ru": [], "zh": [], "sim": []}}
EMPTY_FILES = {"items": {"ru": []}}

# edit operations
EDIT_ADD_PREV_END = "edit_add_prev_end"
EDIT_ADD_NEXT_END = "edit_add_next_end"
EDIT_ADD_CANDIDATE_END = "edit_add_candidate_end"
EDIT_DELETE_LINE = "edit_delete_line"
EDIT_CLEAR_LINE = "edit_clear_line"
EDIT_LINE = "edit_line"
ADD_EMPTY_LINE_BEFORE = "add_empty_line_before"
ADD_EMPTY_LINE_AFTER = "add_empty_line_after"
