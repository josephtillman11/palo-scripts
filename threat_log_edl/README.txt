**This can easily be done in the PAN appliance itself using log-forwarding rules, but I created this for the challenge.**

This Python script pulls specific threat logs (based on user-specified criteria in the request URL) from the Palo Alto XML API and stores them in a file called threat_log.xml. It then extracts source IP addresses from each log entry and stores them in a text file called IP_List.txt. I'm able to use this file as an External Dynamic List (EDL) and create security policies to block these IPs.

