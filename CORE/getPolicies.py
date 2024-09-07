import json
def getPolicy(key,policies_json):
    policies = policies_json
    return policies.get(key,[])