INSERT_CTC_REC = """
INSERT INTO
    ctc_rec (
        id, tick, corr_id, im_doc_no, add_date, due_date, appt_tm,
        cmpl_date, resrc, stat, cgc, enrstat, appr, admstat,
        bctc_no, img_no, app_no, visit_count, sort_ord
    )
VALUES
    (
        {cid}, 'REG', 0, 0, TODAY, TODAY, 0, TODAY, 'SUBMSURV', 'C',
        '', '', '', '', 0, 0, 0, 0, ''
    )
""".format
