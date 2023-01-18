This script does the following:

- Takes 2 inputs: A txt file (must exist in same dir as the script) that contains a list of FQDNs/IP addresses/IP networks and a tag name to tag each address added.
- Verify that the file exists and is not empty
- Use Palo's REST API to see if the tag already exists on the firewall. If it doesn't, then it creates it.
- Add the entries from the text file to a python list.
- Iterate through each list item and create the address object, tagging it with the specified tag. The object string is used as the object name as well.

Use a config.ini file and the configparser module to store things like the API key, firewall hostname, etc.
