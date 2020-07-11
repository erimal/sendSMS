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
        '''SELECT top (10) id,
            MobileNumber,
            MessageToSend 
            FROM datalinx.dbo.exportsms where provider=2''', conn
        )

    df = pd.DataFrame(SQL_Query, columns=['id', 'MobileNumber', 'MessageToSend'])
    #print(df)

    return df

def deliver_message(id):
    date_sent = datetime.today().strftime('%Y-%m-%d')
    SQL = f"update datalinx.dbo.exportsms set DateSent='{date_sent}', SmsSent = 1 where id={id}"
    cursor.execute(SQL)
    conn.commit()

def fail_message(id):
    cursor.execute ("update datalinx.dbo.exportsms set datesent='2020-07-10', smsSent = 1 where id=" + id)