import pyodbc
import settings
from datetime import datetime


# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = settings.DB_SERVER
database = settings.DB_DATABASE
username = settings.DB_USERNAME
password = settings.DB_PASSWORD

# connect to DB tru ODBC driver
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+
                      server+';DATABASE='+
                      database+';UID='+username+';PWD='+ password)

cursor = conn.cursor()

def read_messages():
    cursor.execute('SELECT top (10) id,MobileNumber,MessageToSend FROM datalinx.dbo.exportsms')
    #
    # for row in cursor:
    #     print(row)

    return cursor
def deliver_message(id):
    date_sent = datetime.today().strftime('%Y-%m-%d')
    SQL = f"update datalinx.dbo.exportsms set DateSent='{date_sent}', SmsSent = 1 where id={id}"
    cursor.execute(SQL)
    conn.commit()

def fail_message(id):
    cursor.execute ("update datalinx.dbo.exportsms set datesent='2020-07-10', smsSent = 1 where id=" + id)