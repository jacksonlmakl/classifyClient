import json
def getSecret(key, secrets_json):
    secrets = secrets_json
    return secrets[key]