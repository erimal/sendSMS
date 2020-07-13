import csv
import pandas as pd
import dbConfig

def csvReadme():
    df= pd.read_csv('upload/DayRepayment_new.csv')
    for index, row in df.iterrows():
        id = row['id']
        phone = row['phone']
        msg = row['text']
        print(id)
        dbConfig.add_sms(row)


#read the file
csvReadme()

#Convert the file to get the account and the SMS
#cvswiteSMS