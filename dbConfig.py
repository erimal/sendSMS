import pyodbc
import settings
from datetime import datetime
import pandas as pd

server = settings.DB_SERVER
database = settings.DB_DATABASE
username = settings.DB_USERNAME
password = settings.DB_PASSWORD

# connect to DB tru ODBC driver
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+
                      server+';DATABASE='+
                      database+';UID='+username+';PWD='+ password)

def read_messages():
    SQL_Query = pd.read_sql_query(
        '''SELECT id,
            MobileNumber,
            MessageToSend,
            DateCreated 
            FROM datalinx.dbo.exportsms where provider=2''', conn
        )

    df = pd.DataFrame(SQL_Query, columns=['id', 'MobileNumber', 'MessageToSend', 'DateCreated'])
    #print(df)
    return df

def deliver_message(r,resource_id):
    date_sent = datetime.today().strftime('%Y-%m-%d')

    # update the exportSMS table
    cursor = conn.cursor()
    SQL_u = f"update datalinx.dbo.exportsms set DateSent='{date_sent}', SmsSent = 1 where id={r['id']}"
    cursor.execute(SQL_u)
    conn.commit()

    #insert into the SMSDelivery date
    SQL_i = "insert into datalinx.dbo.SMSDelivery (id, MessageId, MobileNumber,Text,TransactionDate, DateSubmitted, provider) " \
          f"values('{r['id']}', '{resource_id}', '{r['MobileNumber']}', '{r['MessageToSend']}', '{r['DateCreated']}', getdate(), '2')"
    cursor.execute(SQL_i)
    conn.commit()

def fail_message(id):
    cursor.execute ("update datalinx.dbo.exportsms set datesent='2020-07-10', smsSent = 1 where id=" + id)