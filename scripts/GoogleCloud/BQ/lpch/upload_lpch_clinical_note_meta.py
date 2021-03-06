#!/usr/bin/env python2

import os
import logging
import itertools
import string
#import LocalEnv     # used for setting GOOGLE_APPLICATION_CREDENTIALS

from medinfo.db.bigquery import bigQueryUtil
from google.cloud import bigquery

# files names:

# [1] "lpch_clinical_note_meta_121619.csv"
# [1] "ANON_ID"                 "PAT_ENC_CSN_ID_CODED"
# [3] "FILING_DATE_JITTERED"    "NOTE_DATE_JITTERED"
# [5] "ACTIVITY_DATE_JITTERED"  "AUTHOR_PROV_MAP_ID"
# [7] "EFFECTIVE_DEPT_ID"       "NOTE_STATUS_C"
# [9] "NOTE_STATUS"             "AMBULATORY"
# [11] "LTR_STATUS_C"            "LETTER_STATUS"
# [13] "NOTE_TYPE"               "NOTE_TYPE_DESC"
# [15] "EFFECTIVE_TIME_JITTERED" "AUTH_LNKED_PROV_MAP_ID"
# [17] "COSIGN_PROV_MAP_ID"      "DATA_SOURCE"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/Users/jonc101/Downloads/Mining Clinical Decisions-58be3d782c5b.json'

# /Users/jonc101/Downloads/
CSV_FILE_PREFIX = '/Users/jonc101/Downloads/lpch_clinical_note_meta_121619.csv'
csv_path = '/Users/jonc101/Downloads/lpch_clinical_note_meta_121619.csv'

DATASET_NAME = 'lpch'
TABLE_NAME = 'clinical_note_meta'
FINAL_TABLE_SCHEMA = [bigquery.SchemaField('ANON_ID', 'STRING', 'REQUIRED', None, ()),
                      bigquery.SchemaField('PAT_ENC_CSN_ID_CODED', 'STRING', 'REQUIRED', None, ()),
                      bigquery.SchemaField('FILING_DATE_JITTERED', 'DATETIME', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_DATE_JITTERED', 'DATETIME', 'NULLABLE', None, ()),
                      bigquery.SchemaField('ACTIVITY_DATE_JITTERED', 'DATETIME', 'NULLABLE', None, ()),
                      bigquery.SchemaField('AUTHOR_PROV_MAP_ID', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('EFFECTIVE_DEPT_ID', 'INT64', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_STATUS_C', 'INT64', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_STATUS', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('AMBULATORY', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('LTR_STATUS_C', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('LETTER_STATUS', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_TYPE', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_TYPE_DESC', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('EFFECTIVE_TIME_JITTERED', 'DATETIME', 'NULLABLE', None, ()),
                      bigquery.SchemaField('AUTH_LNKED_PROV_MAP_ID', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('COSIGN_PROV_MAP_ID', 'INT64', 'NULLABLE', None, ()),
                      bigquery.SchemaField('DATA_SOURCE', 'STRING', 'NULLABLE', None, ())]

# Final schema is what we want at the end, however, regexp used to process the csv can't handle matching more than 9 fragments (\1 - \9).
# So upload everything as string and process in bigquery - this will take care of string to int and datetime to date conversions
UPLOAD_TABLE_SCHEMA = [bigquery.SchemaField('ANON_ID', 'STRING', 'REQUIRED', None, ()),
                      bigquery.SchemaField('PAT_ENC_CSN_ID_CODED', 'STRING', 'REQUIRED', None, ()),
                      bigquery.SchemaField('FILING_DATE_JITTERED', 'DATETIME', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_DATE_JITTERED', 'DATETIME', 'NULLABLE', None, ()),
                      bigquery.SchemaField('ACTIVITY_DATE_JITTERED', 'DATETIME', 'NULLABLE', None, ()),
                      bigquery.SchemaField('AUTHOR_PROV_MAP_ID', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('EFFECTIVE_DEPT_ID', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_STATUS_C', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_STATUS', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('AMBULATORY', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('LTR_STATUS_C', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('LETTER_STATUS', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_TYPE', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('NOTE_TYPE_DESC', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('EFFECTIVE_TIME_JITTERED', 'DATETIME', 'NULLABLE', None, ()),
                      bigquery.SchemaField('AUTH_LNKED_PROV_MAP_ID', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('COSIGN_PROV_MAP_ID', 'STRING', 'NULLABLE', None, ()),
                      bigquery.SchemaField('DATA_SOURCE', 'STRING', 'NULLABLE', None, ())]




if __name__ == '__main__':
    logging.basicConfig()

    '''
    - removed heading and trailing lines in vim
    - added header line

    split every 2 mln lines:
    split -l 2000000 alert_history_012420.csv alert_history_012420_
    '''
    upload = input('Upload? ("y"/"n"): ')
    bq_client = bigQueryUtil.BigQueryClient()
    if upload == 'Y' or upload == 'y':
        bq_client.reconnect_client()
        bq_client.load_csv_to_table(DATASET_NAME, TABLE_NAME, csv_path, auto_detect_schema=False,
                                    schema=FINAL_TABLE_SCHEMA, skip_rows=1)

    print('Done')

    '''
    expecting 167,058,216 lines from original table
    '''

    '''
    Conversion script in SQL:
create or replace
table alert_2019.alert_history_20200124
as
select * except(
    alt_id_jittered_s,
    alt_csn_id_coded_s,
    alt_status_c_s,
    was_shown_c_s,
    bpa_trgr_action_c_s,
    shown_place_c_s,
    patient_dep_id_s,
    contact_date_time
),
case when alt_id_jittered_s = '' then NULL else cast(alt_id_jittered_s as INT64) end as alt_id_jittered,
case when alt_csn_id_coded_s = '' then NULL else cast(alt_csn_id_coded_s as INT64) end as alt_csn_id_coded,
case when alt_status_c_s = '' then NULL else cast(alt_status_c_s as INT64) end as alt_status_c,
case when was_shown_c_s = '' then NULL else cast(was_shown_c_s as INT64) end as was_shown_c,
case when bpa_trgr_action_c_s = '' then NULL else cast(bpa_trgr_action_c_s as INT64) end as bpa_trgr_action_c,
case when shown_place_c_s = '' then NULL else cast(shown_place_c_s as INT64) end as shown_place_c,
case when patient_dep_id_s = '' then NULL else cast(patient_dep_id_s as INT64) end as patient_dep_id,
cast(contact_date_time as DATE) as contact_date,
timestamp(alt_action_inst, 'America/Los_Angeles') as alt_action_inst_utc
from alert_2019.alert_history_20200124;
    '''
