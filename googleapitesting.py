from pprint import pprint
from googleapiclient.discovery import build

service = build("sheets", "v4")

spreadsheets = service.spreadsheets()
new_sheet_request = spreadsheets.create(body={
    "properties": {
        "title": "Testing Data"
    },
    "sheets": [
        {
            "data": [
                {
                    "rowData": [
                        {
                            "values": [
                                {
                                    "userEnteredValue": {
                                        "stringValue": "A1"
                                    }
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "B1"
                                    }
                                }
                            ]
                        },
                        {
                            "values": [
                                {
                                    "userEnteredValue": {
                                        "stringValue": "A2"
                                    }
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "B2"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ],
})

new_sheet_response = new_sheet_request.execute()
pprint(new_sheet_response["properties"])

service.close()
