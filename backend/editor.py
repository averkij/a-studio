"""Editor query handlers"""

import json
import logging
import sqlite3

import constants as con
import editor_helper
import misc
from lingtrain_aligner import aligner, helper


def edit_doc(
    db_path,
    index_id,
    text,
    operation,
    target,
    candidate_line_id,
    candidate_text,
    batch_id,
    batch_index_id,
    line_id_from,
    line_id_to,
    text_type=con.TYPE_TO,
):
    """Manipulate with document lines"""

    print("starting operation", operation, index_id)
    update_index = True

    with sqlite3.connect(db_path) as db:
        index = aligner.get_doc_index(db)

        if (
            batch_id < 0
            or batch_id >= len(index)
            or batch_index_id < 0
            or batch_index_id > len(index[batch_id])
        ):
            logging.info(
                f"Invalid index coordinates while editing. batch_id: ${batch_id}, batch_index_id: ${batch_index_id}."
            )
            return

        # [3] column in index is processing_to.text_ids
        direction = 3 if text_type == con.TYPE_TO else 1
        line_ids = misc.parse_json_array(index[batch_id][batch_index_id][direction])

        if operation in (con.EDIT_ADD_PREV_END, con.EDIT_ADD_NEXT_END):
            # calculate target cell coordinates
            target_batch_id = batch_id
            if target == "next":
                if batch_index_id + 1 >= len(index[batch_id]):
                    target_batch_id = batch_id + 1
                    target_index_id = 0
                else:
                    target_index_id = batch_index_id + 1
            else:
                if batch_index_id - 1 < 0:
                    if target_batch_id > 0:
                        target_batch_id = batch_id - 1
                        target_index_id = len(index[target_batch_id]) - 1
                    else:
                        logging.warning(
                            f"wrong target coordinates, target_batch_id: ${batch_id - 1}"
                        )
                        return
                else:
                    target_index_id = batch_index_id - 1

            if target_batch_id >= len(index) or target_index_id >= len(
                index[target_batch_id]
            ):
                logging.warning(
                    f"wrong target coordinates, target_batch_id: ${target_batch_id}, target_index_id: ${target_index_id}."
                )
                return

            processing_target_id = index[target_batch_id][target_index_id][0]
            text_to_edit = editor_helper.get_processing_text(
                db_path, text_type, processing_target_id
            )[0]
            text_to_update = text_to_edit + text

            processing_text_ids = misc.parse_json_array(
                index[target_batch_id][target_index_id][direction]
            )
            new_ids = processing_text_ids + line_ids
            new_ids = json.dumps(sorted(list(set(new_ids))))

            # update index ([0]processing_from.id, [1]processing_from.text_ids, [2]processing_to.id, [3]processing_to.text_ids)
            index[target_batch_id][target_index_id][direction] = new_ids
            editor_helper.update_processing(
                db, text_type, processing_target_id, new_ids, text_to_update
            )

        elif operation == con.EDIT_ADD_CANDIDATE_END:
            processing_target_id = index[batch_id][batch_index_id][0]
            text_to_edit = editor_helper.get_processing_text(
                db_path, text_type, processing_target_id
            )[0]
            text_to_update = text_to_edit + candidate_text
            text_to_update = text_to_update.strip()

            processing_text_ids = misc.parse_json_array(
                index[batch_id][batch_index_id][direction]
            )

            new_ids = processing_text_ids + [candidate_line_id]
            new_ids = json.dumps(sorted(list(set(new_ids))))

            index[batch_id][batch_index_id][direction] = new_ids
            editor_helper.update_processing(
                db, text_type, processing_target_id, new_ids, text_to_update
            )

        elif operation == con.ADD_EMPTY_LINE_BEFORE:
            from_id, to_id = editor_helper.add_empty_processing_line(db, batch_id)
            print("from_id", from_id, "to_id", to_id)
            index[batch_id].insert(batch_index_id, (from_id, "[]", to_id, "[]"))

        elif operation == con.ADD_EMPTY_LINE_AFTER:
            from_id, to_id = editor_helper.add_empty_processing_line(db, batch_id)
            print("from_id", from_id, "to_id", to_id)
            index[batch_id].insert(batch_index_id + 1, (from_id, "[]", to_id, "[]"))

        elif operation == con.EDIT_LINE:
            processing_target_id = index[batch_id][batch_index_id][0]
            editor_helper.update_processing(
                db, text_type, processing_target_id, json.dumps(line_ids), text
            )
            update_index = False

        elif operation == con.EDIT_CLEAR_LINE:
            processing_target_id = index[batch_id][batch_index_id][0]
            index[batch_id][batch_index_id][direction] = "[]"
            editor_helper.clear_processing(db, text_type, processing_target_id)

        elif operation == con.EDIT_DELETE_LINE:
            index[batch_id].pop(batch_index_id)
            # TODO should we leave data in processing tables?

        elif operation == con.EDIT_TRY_SET_LINE_IDS:
            lines_to_edit = []

            for bid, batch in enumerate(index):
                for id, line_info in enumerate(batch):
                    if line_info[0] == line_id_from:
                        lines_to_edit.append(
                            {
                                "batch_id": bid,
                                "batch_index_id": id,
                                "line_info": line_info,
                                "update_to": line_id_to,
                            }
                        )
                    elif line_info[0] == line_id_from + 1:
                        lines_to_edit.append(
                            {
                                "batch_id": bid,
                                "batch_index_id": id,
                                "line_info": line_info,
                                "update_to": line_id_to + 1,
                            }
                        )

            print("Trying to split conflict:", lines_to_edit)
            if len(lines_to_edit) < 2:
                logging.warning(
                    f"Can not found two consecutive lines with the given line ids: {line_id_from, line_id_to}"
                )
                return

            direction = 3  # right side (to)

            for line in lines_to_edit:
                processing_target_id = index[line["batch_id"]][line["batch_index_id"]][
                    2
                ]
                new_ids = json.dumps([line["update_to"]])

                text = helper.get_splitted_to_by_id(db_path, [line["update_to"]])
                if not text:
                    logging.warning(
                        f"Can not found text for right side (to) with the following id: {line['update_to']}."
                    )
                    return

                text = text[0][1]  # see get_splitted_to_by_id() in helper

                print(text)

                editor_helper.update_processing(
                    db, con.TYPE_TO, processing_target_id, new_ids, text
                )

                index[line["batch_id"]][line["batch_index_id"]][direction] = new_ids

        else:
            return

        # print("new_ids", new_ids)

        if update_index:
            aligner.update_doc_index(db, index)
