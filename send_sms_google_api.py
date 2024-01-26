from flask import Flask, render_template, request, send_file
import os
from os import getenv
import requests
import json
from googleapiclient.discovery import build
from pprint import pprint


app = Flask(__name__)

@app.get('/')
def messages_templates():
    return render_template('send_msg_template.html')

conversation={} #Dictionary
@app.post('/submit_sms')
def submit_sms():
    # Hi {student_name} are you commimg to class with {reference}. 
    message_template = request.form.get('smsText')
    data= request.form.get('data')

    data=data.replace('\r','')
    rows=data.split('\n')
    keys=rows[0].split(',')

    result=[] #Empty List
    message_List = [] #Empty List
    
   
    for row in rows[1:]:
        values=row.split(',')
        result.append(dict(zip(keys,values)))

    text_belt_api_key = os.environ["TEXT_BELT_API_KEY"] 
    text_belt_api_key =getenv("TEXT_BELT_API_KEY")
    
    for row in result:
        message_to_send=message_template.format(**row)
        phone_target=row['phone'].lstrip().rstrip()
        response=requests.post("https://textbelt.com/text",
        {
            "key": text_belt_api_key ,
            "message": message_to_send,
            "phone": phone_target,
            "replyWebhookUrl": 'https://0db8-2601-681-5a80-430-a977-6d35-af28-dbac.ngrok-free.app/reply'
        }
        )
        confirmation=response.json()
        TextId=confirmation.get("TextId")
        conversation=[TextId]=[]#Set an empty List inside the Dictionary
        conversation[TextId].append({"from":"system","text":message_to_send})

        with open ("conversation.json", "w") as file:
            json.dump(conversation,file,indent=4)

        sucess=confirmation.get("success") # BECAUSE IS A DICT COULD BE json.["success"]) 
        if sucess:
            success_message = 'Your message for {student_name} to {phone} has been submitted successfully!'   
        else:
            success_message = 'Your message for {student_name} to {phone} present an ERROR'
            
        success_message=success_message.format(**row)
        message_List.append(success_message)
        print(response.json()) #To see Json Format of response variable

    successfull_message = 'Log of Messages Sent!'
    createsheet(conversation)
    return render_template('sucess_msg_List.html', success_message=successfull_message, message_templates=message_List)

@app.post("/reply")
def reply():
    reply=request.json
    textId=reply.get("textId")
    conversation.get(textId).append({"from":reply.get("fromNumber"),"text":reply.get("fromNumber")})

    with open ("conversation.json", "w") as file:
            json.dump(conversation,file,indent=4)
            
    createsheet(conversation)
    return "OK"


def createsheet(conversation):   
    service = build("sheets", "v4")
    
    # Create a new spreadsheet
    spreadsheet = service.spreadsheets().create(body={
        'properties': {'title': 'List of Messages'}
    }).execute()
    
    # Get the spreadsheet ID
    spreadsheet_id = spreadsheet['spreadsheetId']
    
    # The range where you want to append the data (e.g., Sheet1!A1:B1)
    range_ = 'Sheet1!A2:D'

    # The data you want to append
    values = [[row['TextId'], row['from'], row['text']] for row in conversation]
    
    # Append the data to the sheet
    request = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_,
        body={'values': values},
        valueInputOption='RAW'
    )

    response = request.execute()

    service.close()



if __name__ == '__main__':
    app.run(debug=True,port=8001) 

#open web browser  and navigate :  http://localhost:8001/

#Install ngrok firts Create a Account then log in to the account in the terminal

# **Installing Libraries Client - python
# pip install --upgrade google-api-python-client

# **Install python extension//  Python Extension Pack -- Popular Visual Studio Code extensions for Python

# ***Download GoogleCloudSDKInstaller and Execute it

# **Build a Google Service
#from googleapiclient.discovery import build

#service = build('drive', 'v3')
## ...
#service.close()





