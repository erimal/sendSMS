import mysql.connector
import settings
from datetime import datetime
import pandas as pd

# connect to DB
conn = mysql.connector.connect(
  host=settings.DB_SERVER,
  user=settings.DB_USERNAME,
  password=settings.DB_PASSWORD,
  database=settings.DB_DATABASE
)
cursor = conn.cursor()

def read_messages():
    SQL_Query = pd.read_sql_query(
        '''select id,mobilenumber,message,datecreated from uploadapp_smsimported where sent=0 and provider=2''', conn
        )

    df = pd.DataFrame(SQL_Query, columns=['id', 'mobilenumber', 'message', 'datecreated'])
    #print(df)
    return df

def deliver_message(r,resource_id):
    date_sent = datetime.today() #.strftime('%Y-%m-%d')

    # update the import table
    SQL_u = f"update uploadapp_smsimported set datesent='{date_sent}', sent = 1 , attempt = 1 where id={r['id']}"
    cursor.execute(SQL_u)
    conn.commit()

    #insert into the SMSDelivery date
    SQL_i = "insert into uploadapp_smsdelivered (smsimported_id, messageId, mobilenumber,message, datesubmitted, provider,delivered,user_id) " \
          f"values('{r['id']}', '{resource_id}', '{r['mobilenumber']}', '{r['message']}', '{date_sent}', '2','0','1')"
    #print("SQL to insert: " + SQL_i)
    cursor.execute(SQL_i)
    conn.commit()

# def fail_message(id):
#     cursor.execute ("update datalinx.dbo.exportsms set datesent='2020-07-10', smsSent = 1 where id=" + id)

def add_sms(r):
    datecreated = datetime.today().strftime('%Y-%m-%d')
    SQL_i = "insert into smsimported (other_id,	mobilenumber, message,datecreated,sent,attempt,provider) " \
            f"values('{r['id']}', '{r['phone']}', '{r['text']}', '{datecreated}','0','0', '2')"
    # print("SQL to insert: " + SQL_i)
    cursor.execute(SQL_i)
    conn.commit()