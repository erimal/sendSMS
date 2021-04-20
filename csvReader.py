#This program reads a file in the upload folder. the name of the file is sms.csv
# The file has the following format  headers : id,phone,text
#The file is updated in the database configured in the setting.py
#
# author Eric Malm  Date june-2020

import pandas as pd
import dbConfig

def csvReadme():
    df= pd.read_csv('upload/sms.csv')
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