"""Alignment processor"""

import logging
import queue
import sqlite3
import time
from multiprocessing import Process, Queue

import constants as con
import matplotlib
import user_db_helper
from lingtrain_aligner import aligner, resolver, vis_helper

# https://stackoverflow.com/questions/49921721/runtimeerror-main-thread-is-not-in-main-loop-with-matplotlib-and-flask
matplotlib.use('Agg')


FINISH_PROCESS = "finish_process"


class AlignmentProcessor:
    """Processor with parallel texts alignment logic"""

    def __init__(self, proc_count, db_path, user_db_path, res_img_best, lang_name_from, lang_name_to, align_guid, model_name, window, embed_batch_size, normalize_embeddings, mode="align"):
        self.proc_count = proc_count
        self.queue_in = Queue()
        self.queue_out = Queue()
        self.db_path = db_path
        self.user_db_path = user_db_path
        self.res_img_best = res_img_best
        self.lang_name_from = lang_name_from
        self.lang_name_to = lang_name_to
        self.tasks_count = 0
        self.align_guid = align_guid
        self.model_name = model_name
        self.window = window
        self.mode = mode
        self.embed_batch_size = embed_batch_size
        self.normalize_embeddings = normalize_embeddings

    def add_tasks(self, task_list):
        """Add batches with string arrays for the further processing"""
        for i, task in enumerate(task_list):
            self.queue_in.put((i, task))
        for i in range(self.proc_count):
            self.queue_in.put((-1, FINISH_PROCESS))
        self.tasks_count = len(task_list)

    def work(self, queue_in, queue_out):
        """Create separate alignment processes"""
        while True:
            try:
                task_index, task = queue_in.get_nowait()
            except queue.Empty:
                print(
                    'found an empty queue. Sleeping for a while before checking again...')
                time.sleep(0.01)
            else:
                try:
                    if task == FINISH_PROCESS:
                        print('No more work left to be done. Exiting...')
                        break

                    print("task_index", task_index)

                    if self.mode == "align":
                        self.process_batch_wrapper(*task)
                    elif self.mode =="resolve":
                        self.resolve_batch_wrapper(task)

                except Exception as e:
                    print('task failed. ' + str(e))
                    queue_out.put("error")

    def handle_result(self, queue_out):
        """Handle the result of a single finished process"""
        counter = 0
        error_occured = False
        result = []

        while counter < self.tasks_count:
            result_code, batch_number, texts_from, texts_to = queue_out.get()

            if result_code == con.PROC_DONE:
                result.append((batch_number, texts_from, texts_to))
                with sqlite3.connect(self.db_path) as db:
                    aligner.update_batch_progress(db, batch_number)
                user_db_helper.increment_alignment_state(
                    self.db_path, self.user_db_path, self.align_guid, con.PROC_IN_PROGRESS)

            elif result_code == con.PROC_ERROR:
                error_occured = True
                user_db_helper.increment_alignment_state(
                    self.db_path, self.user_db_path, self.align_guid, con.PROC_ERROR)
                break

            counter += 1

        # sort by batch_id
        result.sort()
        with sqlite3.connect(self.db_path) as db:
            logging.info(f"writing {len(result)} batches to {self.db_path}")
            aligner.rewrite_processing_batches(db, result)

            logging.info(f"creating index for {self.db_path}")
            aligner.create_doc_index(db, result)

        for batch_id, _, _ in result:
            vis_helper.visualize_alignment_by_db(
                self.db_path, self.res_img_best, lang_name_from=self.lang_name_from, lang_name_to=self.lang_name_to, batch_ids=[batch_id], transparent_bg=True)

        if not error_occured:
            print("finishing. no error occured")
            curr_batches, total_batches = user_db_helper.get_alignment_progress(self.user_db_path, self.align_guid)
            if (curr_batches == total_batches):
                user_db_helper.update_alignment_state(
                    self.user_db_path, self.align_guid, con.PROC_DONE)
            else:
                user_db_helper.update_alignment_state(
                    self.user_db_path, self.align_guid, con.PROC_IN_PROGRESS_DONE)
        else:
            print("finishing with error")

    def start_align(self):
        """Start workers"""
        align_handler = Process(
            target=self.handle_result, args=(self.queue_out,), daemon=True)
        align_handler.start()

        workers = [Process(target=self.work, args=(self.queue_in, self.queue_out), daemon=True) for _ in range(
            min(self.proc_count, self.tasks_count))]  # do not run more processes than necessary
        for w in workers:
            w.start()
    
    def process_batch_wrapper(self, lines_from_batch, lines_to_batch, line_ids_from, line_ids_to, batch_number):
        """Align process wrapper"""
        logging.info(f"Alignment started for {self.db_path}.")
        try:
            texts_from, texts_to = aligner.process_batch(lines_from_batch, lines_to_batch, line_ids_from, line_ids_to, batch_number, self.model_name, self.window, self.embed_batch_size, self.normalize_embeddings, show_progress_bar=False,
                                                         save_pic=True, lang_name_from=self.lang_name_from, lang_name_to=self.lang_name_to, img_path=self.res_img_best)
            self.queue_out.put(
                (con.PROC_DONE, batch_number, texts_from, texts_to))
        except Exception as e:
            logging.error(e, exc_info=True)
            self.queue_out.put((con.PROC_ERROR, [], [], []))

    def start_resolve(self):
        """Start resolve workers"""
        resolve_handler = Process(
            target=self.handle_resolve, args=(self.queue_out,), daemon=True)
        resolve_handler.start()

        workers = [Process(target=self.work, args=(self.queue_in, self.queue_out), daemon=True) for _ in range(
            min(self.proc_count, self.tasks_count))]  # do not run more processes than necessary
        for w in workers:
            w.start()

    def resolve_batch_wrapper(self, batch_id):
        """Resolve conflicts wrapper"""
        logging.info(f"Conflicts resolving started for {self.db_path}.")
        try:
            #conflicts resolving strategy
            steps = 3
            print("resolving conflicts strategy 1. batch_id:", batch_id)

            for i in range(steps):
                conflicts, _ = resolver.get_all_conflicts(
                    self.db_path, min_chain_length=2+i, max_conflicts_len=6*(i+1), batch_id=batch_id)
                resolver.resolve_all_conflicts(
                    self.db_path, conflicts, self.model_name, show_logs=False)

            print("resolving conflicts strategy 2. batch_id:", batch_id)
            conflicts, _ = resolver.get_all_conflicts(
                self.db_path, min_chain_length=2, max_conflicts_len=18, batch_id=batch_id)
            resolver.resolve_all_conflicts(
                self.db_path, conflicts, self.model_name, show_logs=False)

            self.queue_out.put(
                (con.PROC_DONE, batch_id))

        except Exception as e:
            logging.error(e, exc_info=True)
            self.queue_out.put((con.PROC_ERROR, []))

    def handle_resolve(self, queue_out):
        """Handle the result of a single finished process"""
        counter = 0
        error_occured = False
        result = []
        
        while counter < self.tasks_count:
            result_code, batch_number = queue_out.get()            
            if result_code == con.PROC_DONE:
                result.append(batch_number)
            elif result_code == con.PROC_ERROR:
                error_occured = True
                user_db_helper.increment_alignment_state(
                    self.db_path, self.user_db_path, self.align_guid, con.PROC_ERROR)
                break
            counter += 1

        vis_helper.visualize_alignment_by_db(
                self.db_path, self.res_img_best, lang_name_from=self.lang_name_from, lang_name_to=self.lang_name_to, batch_ids=result, transparent_bg=True)

        if not error_occured:
            print("finishing. no error occured")
            curr_batches, total_batches = user_db_helper.get_alignment_progress(self.user_db_path, self.align_guid)
            if (curr_batches == total_batches):
                user_db_helper.update_alignment_state(
                    self.user_db_path, self.align_guid, con.DONE_FOLDER)
            else:
                user_db_helper.update_alignment_state(
                    self.user_db_path, self.align_guid, con.PROC_IN_PROGRESS_DONE)
        else:
            print("finishing with error")
