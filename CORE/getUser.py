import json
def getUser(key,users_json):
    secrets = users_json
    return secrets[key]