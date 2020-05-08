from google.cloud import bigquery
from medinfo.db.bigquery import bigQueryUtil
import datetime
import pandas
import sys 
import time

bq_client = bigQueryUtil.BigQueryClient()

# sleep  time 
a1 = sys.argv[1] 

# letter that you searching for  first 
a2 = sys.argv[2]

# number of rows
a3 = sys.argv[3]


sql = ["select count(med_description) as med_count, med_description from datalake_47618.order_med where lower(med_description) like \'"  , a2 , "%' group by med_description order by med_count  desc limit ", a3 ]
sql1 = ''.join(sql)
query1 = bq_client.queryBQ(sql1)
df = query1.to_dataframe()

for row_index,row in df.iterrows():
   print('\nrow number:',row_index, '\n-------------') 
   time.sleep(float(a1))
   print(row)
