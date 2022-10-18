import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
 
def create_job():
    now = datetime.now()
    curr_time = now.strftime("%Y/%m/%d %H:%M:%S")
    prev_time = now - timedelta(hours=12, minutes=0)
    prev_time = prev_time.strftime("%Y/%m/%d %H:%M:%S")
    
    
    host = '1.2.3.4'
    url = "https://{}/api/?type=log&log-type=threat&query=( (receive_time leq '{}') and (receive_time geq '{}') and ( zone.src eq outside ) and ( zone.dst eq outside ) and ( subtype eq vulnerability ))".format(host, curr_time, prev_time)
    header = {'Accept': "application/json",
        'X-PAN-KEY': "abcdefghijklmnopqrstuvwxyz"}
    
    r = requests.get(url, headers=header, verify=False)
 
    root = ET.fromstring(r.content)
    
    time.sleep(10)
    
    job_id = root[0][1].text
        
    return job_id
 
def make_list(job):
    job_id = job
    host = '1.2.3.4'
    url = "https://{}/api/?type=log&action=get&job-id={}".format(host, job_id)
    header = {'Accept': "application/json",
    'X-PAN-KEY': "abcdefghijklmnopqrstuvwxyz"}
 
    r = requests.get(url, headers=header, verify=False)
    
    with open('threat_log.xml', 'wb') as f:
        f.write(r.content)
    
    tree = ET.parse('threat_log.xml')
    
    root = tree.getroot()
    
    nf = open("IP_List.txt", "a")
    
    for x in root.findall('result/log/logs/entry'):
        ip = x.find('src').text
        nf.write(ip + '\n')
 
make_list(create_job())
