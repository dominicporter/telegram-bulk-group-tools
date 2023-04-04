# Telegram Bulk Group Generation

These scripts use the API TO:
- scrap all the users from one of your groups to a csv file
- generate many telegram groups with the initial user list as admins
- delete the groups when you are done with them (TODO)

## Setup API

Go to http://my.telegram.org and log in.
Click on API development tools and fill the required fields.
put app name you want & select other in platform Example :
copy "api_id" & "api_hash" after clicking create app ( will be used in setup.py )

## How To Install
```
$ pkg install -y git python

$ git clone https://github.com/dominicporter/telegram-bulk-group-tools

$ cd telegram-bulk-group-tools

$ chmod +x * && python3 setup.py

$ python3 setup.py
```


## To Generate User Data
```
$ python3 scraper.py
```

## Creating your groups
- Edit `BulkCreateGroups.py` to use your own Team Names etc

```
$ python3 BulkCreateGroups.py
```

- This will put the names and Ids of all the groups into `createdGroups.csv` (for later use when deleting)

## Deleting the groups
- Make sure you have the groups to be deleted in `createdGroups.csv`

```
$ python3 BulkDeleteGroups.py
```
