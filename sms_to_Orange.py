
import smpplib
import settings
import dbConfig
import json , requests
import pandas as pd

client = None
url = 'https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B23100000000/requests'
df = dbConfig.read_messages()

# for index, row in df.iterrows():
#     print(row['id'], row['MobileNumber'])
# dbConfig.deliver_message('3')
try:
        for index, row in df.iterrows():
           # print(row['id'], row['MobileNumber'],row['MessageToSend'])
            phone = row['MobileNumber']
            msg = row['MessageToSend']

        # first data value for JSON
        data = {}
        data['address'] = 'tel:+' + phone
        data['senderName'] = 'Accessbank'
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

        print(json_data_final)

        body = {
            "outboundSMSMessageRequest": {
                "address": "tel:+231881551966",
                "senderName": "Accessbank",
                "senderAddress": "tel:+23100000000",
                "outboundSMSTextMessage": {
                    "message": "Hello, this is a test from Eric Malm with Orange API 3"
                }
            }
        }

        header = {
                    "Authorization": "Bearer MCUbVN3BnnVakzjEoDwejPqDBduJ",
                    "Content-Type": "application/json"
                 }

        response = requests.post(url, json_data_final, headers=header)

        print(response.text)
        if response.status_code == '201':
            print("Message Delivered")
        else:
            print("Status code: ", response.status_code)
            
        #print("Printing Entire Post Request")
        #print(response.json())

except ConnectionError as con_error:
        print('connecton issue: ' + con_error)
finally:
        if client:
                #print "==client.state====", client.state
                #client.disconnect()
                #print "==client.state====", client.state
                print ('this is the end of the code ')
        else:
                print ('Connedction to SMS Gateway Failed')