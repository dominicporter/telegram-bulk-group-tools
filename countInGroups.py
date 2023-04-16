from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
 
groups=[]
 
for dialog in client.iter_dialogs():
    if " TBOStwds" in dialog.title:
        groups.append(dialog)

groups.sort(key=lambda group: group.title)

print(gr+'[+] Saving In file...')
time.sleep(1)
with open("stewardGroupCounts.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['groupName','memberCount'])
    for g in groups:
        participants = client.get_participants(g)
        print('{} - {}'.format(g.title, len(participants)))

        writer.writerow([g.title,len(participants)])      
print(gr+'[+] Saved in stewardGroupCounts.csv')