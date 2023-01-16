import os, sys
import json
import requests
import configparser
from requests.exceptions import RequestException

# Store values in config.ini
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['api']['key']
firewallAddress = config['firewall']['address']
panVersion = config['firewall']['version']
vsys = config['firewall']['vsys']

tagEndpoint = f"https://{firewallAddress}:/restapi/{panVersion}/Objects/Tags?location=vsys&vsys={vsys}&name="
addressEndpoint = f"https://{firewallAddress}:/restapi/{panVersion}/Objects/Addresses?location=vsys&vsys={vsys}&name="
payload = ""
headers = {
'Accept': 'application/json',
'X-PAN-KEY': api_key,
'Content-Type': 'application/json'
}
listItems = []

def validateTag(statusCode):
    if statusCode == 200:
        return True
        print('Status code is 200')
    elif statusCode == 404:
        return False
        print('Status code is 404')
    else:
        print('Error ' + statusCode)
        sys.exit()

def createTag(tagName):
    # Create tag
    payload = json.dumps({
        "entry": [
            {
                "@name": tagName
            }
        ]
    })
    try:
        response = requests.request("POST", tagEndpoint+tagName, headers=headers, data=payload, verify=False)
        if response.status_code != 200:
            print(f'Error: {response.status_code}')
            return
    except RequestException as e:
        print(f'Error: {e}')
        return
    print('Created tag '+tagName)

def createObject(textFile, tagName):
    # Verify text file exists and is not empty
    fileExists = False
    try:
        if os.path.getsize(textFile) > 0:
            fileExists = True
            print('The file ' + textFile + ' exists and is not empty!')
        else:
            print('File is empty!')
            sys.exit()
    except OSError as e:
        print('File does not exist or is not accessible!')
        sys.exit()
    
    if fileExists:
        # Connect to firewall and see if tag exists
        try:
            response = requests.request("GET", tagEndpoint+tagName, headers=headers, data="", verify=False)
        except RequestException as e:
            print(f'Error: {e}')
            return
        tagExists = validateTag(response.status_code)
        # If tag doesn't exist, create it
        if tagExists == False:
            createTag(tagName)
        else:
            print('Using existing tag ' + tagName)

        # Populate listItems from text file
        with open (textFile) as f:
            for line in map(str.strip, f):
                if line == "":
                    continue
                listItems.append(line)
        
        # Create the address objects using the url list
        for line in listItems:
            payload = json.dumps({
            "entry": [
                {
                "@name": line,
                "@location": "vsys",
                "@vsys": vsys,
                "fqdn": line,
                "tag": {
                    "member": [
                        tagName
                    ]
                }
                }
            ]
            })
            try:
                response = requests.request("POST", addressEndpoint+line, headers=headers, data=payload, verify=False)
            except RequestException as e:
                print (f"Error: {e}")
                return 

if __name__ == "__main__":
    createObject('objectList.txt', 'my-tag')
