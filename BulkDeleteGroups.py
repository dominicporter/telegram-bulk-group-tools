from telethon.sync import TelegramClient
from telethon.tl.functions.messages import (
    GetDialogsRequest,
    CreateChatRequest,
    ExportChatInviteRequest,
    EditChatAboutRequest,
)
from telethon.tl.types import (
    InputPeerEmpty,
    InputPeerChannel,
    InputPeerUser,
    ChatAdminRights,
    InputChannel,
)
from telethon.errors.rpcerrorlist import UserNotParticipantError, ChannelPrivateError
from telethon.tl.functions.channels import (
    InviteToChannelRequest,
    EditAdminRequest,
    CreateChannelRequest,
    DeleteChannelRequest,
)
import sys
import csv
import traceback
import time
import random
import configparser

cpass = configparser.RawConfigParser()
cpass.read("config.data")

try:
    api_id = cpass["cred"]["id"]
    api_hash = cpass["cred"]["hash"]
    phone = cpass["cred"]["phone"]
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system("clear")
    banner()
    print(re + "[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input(gr + "[+] Enter the code: " + re))

groups = []
with open(r"createdGroups.csv", encoding="UTF-8") as f:  # Enter your file name
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    #     next(rows, None)
    for row in rows:
        group = {}
        group["id"] = int(row[0])
        group["access_hash"] = int(row[1])
        group["name"] = row[2]
        groups.append(group)


def deleteGroup(groupId, accessHash):
    entity = InputChannel(groupId, accessHash)
    print(entity)
    result = client(DeleteChannelRequest(entity))
    print(result)

for group in groups:
    print(group)

    try:
        deleteGroup(group["id"], group["access_hash"])
    except ChannelPrivateError:
        print("failed to delete " + group["name"] + ", maybe already deleted?")
