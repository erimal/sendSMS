import settings
import dbConfig
import json
import requests
import pandas as pd
import logging
from datetime import datetime

client = None
url = 'https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B23100000000/requests'
df = dbConfig.read_messages()

#Create an error  log file
file_log = settings.LOG_FILENAME + "_" + (datetime.now().strftime("%Y-%m-%d"))

logging.basicConfig(format='Date-Time : %(asctime)s : %(message)s',
                    level=logging.INFO, filename=file_log, filemode='a')

try:
        for index, row in df.iterrows():
            phone = row['mobilenumber']
            msg = row['message']

            # first data value for JSON
            data = {}
            data['address'] = 'tel:+' + phone
            #data['address'] = 'tel:+23177'
            data['senderName'] = 'ACCESSBANK'
            data['senderAddress'] = "tel:+23100000000"

            # Json data value
            data_msg = {}
            data_msg['message'] = msg

            #Add phone numbers ,sender name , sender address to the message
            data['outboundSMSTextMessage'] = data_msg

            # Add the first part of the message to the final outboundSMSMessageRequest message
            data_final = {}
            data_final['outboundSMSMessageRequest'] = data
            json_data_final = json.dumps(data_final)

            #print(json_data_final)
            header = {
                        "Authorization": "Bearer MCUbVN3BnnVakzjEoDwejPqDBduJ",
                        "Content-Type": "application/json"
                     }

            response = requests.post(url, json_data_final, headers=header)

            if response.status_code == 201:

                #print(response.text)
                resp_text = json.loads(response.text)
                resource_url = resp_text['outboundSMSMessageRequest']['resourceURL']
                resource_id = resource_url[-36:]
                print("Message Delivered to Phone:" + phone + " with resource Id: " + resource_id)

                #update the export SMS table
                dbConfig.deliver_message(row, resource_id)
            else:
                print("Delivery failed Status code: ", response.status_code)

                logging.info('Delivery failed: response code:{} - phone:{}'.format(response.status_code, phone))

except Exception as exception:
    assert type(exception).__name__ == 'NameError'
    assert exception.__class__.__name__ == 'NameError'
    assert exception.__class__.__qualname__ == 'NameError'
