from flask import Flask, render_template, request, send_file
import os
from os import getenv
import requests
import json
from googleapiclient.discovery import build
import gspread
from pprint import pprint

app = Flask(__name__)
 # Hi {student_name} are you commimg to class with {reference}. 
@app.get('/')
def messages_templates():
    return render_template('send_msg_template.html')

conversation = {}  # Initialize an empty dictionary for conversation

@app.post('/submit_sms')
def submit_sms():
    message_template = request.form.get('smsText')
    data = request.form.get('data')

    data = data.replace('\r', '')
    rows = data.split('\n')
    keys = rows[0].split(',')
    result = []  # Empty List

    for row in rows[1:]:
        values = row.split(',')
        result.append(dict(zip(keys, values)))

    text_belt_api_key = os.environ["TEXT_BELT_API_KEY"] 
    text_belt_api_key =getenv("TEXT_BELT_API_KEY")

    message_List = []  # Initialize an empty list for messages

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
        TextId=confirmation.get("textId")
            
        if TextId:
           if TextId not in conversation:
                conversation[TextId] = []
        conversation[TextId].append({"from": "system", "text": message_to_send})
        
    
        # Write the conversation dictionary to a JSON file
        with open("conversation.json", "w") as file:
            json.dump(conversation, file, indent=4)

        success = confirmation.get("success")
        if success:
            success_message = f'Your message for {row["student_name"]} to {row["phone"]} has been submitted successfully!'
        else:
            success_message = f'Your message for {row["student_name"]} to {row["phone"]} present an ERROR'

        message_List.append(success_message)

    successful_message = 'Log of Messages Sent!'
    createsheet()
    return render_template('sucess_msg_List.html', success_message=successful_message, message_templates=message_List)
    
    
@app.post("/reply")
def reply():
    reply = request.json
    textId = reply.get("textId")

    if textId not in conversation:
        conversation[textId] = []  # Initialize an empty list for the TextId

    conversation[textId].append({"from": reply.get("fromNumber"), "text": reply.get("fromNumber")})

    with open("conversation.json", "w") as file:
        json.dump(conversation, file, indent=4)

    createsheet()
    return "OK"


def createsheet():
    # Load conversation data from the JSON file
    with open("conversation.json", "r") as file:
        conversation_data = json.load(file)
   
    
    service = build('sheets', 'v4')

    # Check if the spreadsheet already exists
    spreadsheet_title = 'List of Messages'
    spreadsheet_exists = False
    
   
    # Create a new spreadsheet
    spreadsheet = service.spreadsheets().create(body={
            'properties': {'title': spreadsheet_title}
    }).execute()
        
    # Get the spreadsheet ID
    spreadsheet_id = spreadsheet['spreadsheetId']
    
    
    # Define the header row
    header_row = ["TextId", "From", "Message"]

    # Extract values from the conversation dictionary
    values = [header_row]  # Start with the header row
    values.extend([[TextId, msg["from"], msg["text"]] for TextId, msgs in conversation_data.items() for msg in msgs])
    print("Values extracted from conversation data:", values)  # Debug print
    
    # The range where to append the data
    range_ = 'Hoja 1!A1:C'  

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
