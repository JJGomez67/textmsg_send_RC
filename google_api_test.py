
import gspread
from gspread.auth import Credentials
#from gspread import oauth

# Set up the API key
myapi_key = 'AIzaSyBXdFkIATkkehLuUNOi2itDYmIeWsI8ZLc'
creds = Credentials.from_api_key('myapi_key')
client = gspread.Client(auth=creds)


# **Installing Libraries Client - python
# pip install --upgrade google-api-python-client
# pip install gspread



# Authorize the client object
#client = gspread.authorize(api_key)
# Authenticate client object using API Key
#client = gspread.service_account(api_key)

# Authenticate using an API key
#client = gspread.oauth(api_key='AIzaSyBXdFkIATkkehLuUNOi2itDYmIeWsI8ZLc')
#client =gspread.oauth(no_service_account=True, api_key=myapi_key)
#client =gspread.Client(auth='api_key', api_key=myapi_key)

# Open a spreadsheet by its title
sh = client.open('My Spreadsheet')

# Create a new worksheet
worksheet = sh.add_worksheet(title='New Worksheet', rows=100, cols=20)

# Write data to a cell
worksheet.update('A1', 'Hello World')

# Read data from a cell
cell_value = worksheet.acell('A1').value

# Delete a worksheet
#sh.del_worksheet(worksheet)

if __name__ == '__main__':
    app.run(debug=True,port=8001) 