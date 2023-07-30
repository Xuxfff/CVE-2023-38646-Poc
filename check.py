import requests
import sys
import re

def check(ip, port):
    url = f"http://{ip}:{port}"
    try:
        rep = requests.get(url + "/api/session/properties",timeout=3).text
        token = re.search(r'"setup-token":"(.*?)"',rep)
        if not token:
            return False
        token = token.group(1)
        t = {"token":token,"details":{"is_on_demand":False,"is_full_sync":False,"is_sample":False,"cache_ttl":None,"refingerprint":True,"auto_run_queries":True,"schedules":{},"details":{},"name":"test","engine":"mysql"}}
        rep = requests.post(url=url+"/api/setup/validate",json=t,timeout=3)
        if (any('metabase' in val for val in rep.headers.values())) and 'Instance already initialized' not in rep.text and ('Could not connect to address' in rep.text or ('message' in rep.text and 'errors' in rep.text and 'host' in rep.text)):
            return True
        return False
    except:
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit("usage: python check.py ip port")
    ip, port = sys.argv[1], sys.argv[2]
    if check(ip, port):
        print(f"[+] check {ip}:{port} CVE-2023-38646 Exists!")
    else:
        print(f"[-]check {ip}:{port} CVE-2023-38646 Not Exists!")