import json
def getAppSecret(key):
    with open('appSecrets.json', 'r') as f:
        config = json.load(f)
        secrets = config
        return secrets[key]