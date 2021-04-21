#!/usr/bin/env python3

#  Searches for inactive users and activates those accounts
#
#

import csv
import requests
import sys

# Connect to UEM
# AuthHeader uses Svc Acct
# BaseURL
BaseURL="https://as1688.awmdm.com/API"
headers = {
  'aw-tenant-code': 'nn3kmW6SImGvaEPUqjGukHkk51LBFt5AIl4c4r3JJ+c=',
  'Content-Type': 'application/json;version=2',
  'Authorization': 'Basic a3VydC5vc3Ryb206U21hY2tvdXQyMDIyIQ==',
  'Cookie': 'WS1UEMCOOKIE=!HfCfLfMYE/F1vZyxAj7Pd2JBL+2tfcojAwZfYz8t1WKbNj4gaaWYuAgNuwZ0FGfy6z9gV7kimGTQ9YA='
}

# Search for inactive users
response = requests.get(BaseURL + "/system/users/search?pagesize=10000&status=Inactive", headers=headers, timeout=30)

# Variable stores the JSON response
data = response.json()
# Gets all user data
user_data = data["Users"]
#print(data)


# Pasring the data
for user in user_data:
    #print(f"{user['UserName']}, {user['Status']}, {user['Id']['Value']}")
    username = user['UserName']
    user_status = user['Status']
    user_id = user['Id']['Value']
    payload = """{'BulkValues': {'Value': [%s]}}""" % user_id
    if user_status is False:
        print(f"Activating user: {username}")
        response = requests.post(BaseURL + "/system/users/activate", headers=headers, timeout=30, data=payload)
        status_code = response.status_code
        print(status_code)
