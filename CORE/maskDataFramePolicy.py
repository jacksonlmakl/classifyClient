from CORE.mask import maskData
from CORE.getPolicies import getPolicy

def maskDataPolicy(data,policies,tags=None,policies_json={}, users_json={}, secrets_json={}):
    x=[]
    for policy in policies:
        i=getPolicy(policy,policies_json)
        x=x+i
    output=maskData(data=data,allowed_tags=x,tags=tags,secrets_json=secrets_json)
    return output