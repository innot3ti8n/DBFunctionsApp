import json
import os

with open('./local.settings.json') as lfile:
    localSettings = json.load(lfile)

for i in localSettings['Values']:
    os.environ[i] = localSettings['Values'][i]