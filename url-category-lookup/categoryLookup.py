import sys
import Constants
import requests
import xml.etree.ElementTree as ET
import ipaddress,socket


host = Constants.PAN_HOST
url = sys.argv[1]
key = Constants.PAN_API_KEY

def checkUrl (url):
    r = requests.get(f'https://{host}/api/?type=op&cmd=<test><url>{url}</url></test>&key={key}', verify=True)
    root = ET.fromstring(r.text)

    try:
        ip_object = ipaddress.ip_address(url)
        print(f"{url} is an IP address - doing reverse lookup...")

        name, alias, addresslist = socket.gethostbyaddr(url)
        print(f'Reverse lookup: {name}')

    except ValueError:
        print(f"{url} is not an IP address, therefore reverse lookup wont be done.")

    category = root[0].text.replace("\n", "")
    parsed = category.split(" ")
    category = parsed[-4] + " " + parsed [-3] + " " + parsed[-2]+ " " + parsed[-1]

    print(f"The URL is categorized as: {category}")

if __name__ == "__main__":
    checkUrl(url)
