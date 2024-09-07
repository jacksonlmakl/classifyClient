from CORE.postgres import sql
from CORE.maskDataFramePolicy import maskDataPolicy
from CORE.getPolicies import getPolicy
from CORE.autoClassifyDataFrame import autoClassify
from CORE.getUser import getUser

def userDataFrame(email,df,policies_json, users_json, secrets_json):
    return maskDataPolicy(df,getUser(email,users_json).get('allowed_policies'),None,policies_json, users_json, secrets_json)


