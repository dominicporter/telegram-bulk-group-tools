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
)
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import (
    InviteToChannelRequest,
    EditAdminRequest,
    CreateChannelRequest,
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

users = []
with open(r"members.csv", encoding="UTF-8") as f:  # Enter your file name
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user["username"] = row[0]
        user["id"] = int(row[1])
        user["access_hash"] = int(row[2])
        user["name"] = row[3]
        users.append(user)


def createGroup(groupName):
    # Create the Group
    result = client(
        CreateChannelRequest(title=groupName, about="", broadcast=False, megagroup=True)
    )
    chat = result.chats[0]

    # Set some permissions for all
    client.edit_permissions(chat, invite_users=True, change_info=False)

    # Get the invite link and add it to header
    inviteLink = client(
        ExportChatInviteRequest(
            peer=chat,
            legacy_revoke_permanent=True,
            request_needed=True,
        )
    ).link

    # Write chat details to file
    with open("createdGroups.csv", "a", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow([chat.id, chat.access_hash, chat.title, inviteLink])

    result = client(EditChatAboutRequest(peer=chat, about="Invite Link: " + inviteLink))

    # Give admin to all users in members.csv
    for user in users:
        try:
            result = client.edit_admin(
                chat.id, client.get_entity(user["id"]), is_admin=True, anonymous=False
            )
            time.sleep(0.2)
        except UserNotParticipantError:
            print("User not a member so can't be made admin: " + user["name"])


groupNames = []
with open(r"teamNames.txt", encoding="UTF-8") as f:  # Enter your file name
    rows = f.readlines()
    for row in rows:
        groupNames.append(row.rstrip())

# This will generate one group for each name and each prefix, so if there are 100 groupNames and 4 prefixes, it will make 400 groups
prefixes = ["Fri", "Sat", "Sun", "Mon"]
suffix = "TBOStwds"
for name in groupNames:
    for prefix in prefixes:
        groupName = prefix + " " + name + " " + suffix
        createGroup(groupName)
        # print(groupName) # Dry run
        time.sleep(60)
