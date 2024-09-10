from CORE.autoClassifyDataFrame import autoClassify
import pandas as pd
from CORE.postgres import *
from CORE.getPolicies import getPolicy

def maskData(data,allowed_tags,tags=None,secrets_json={}):
    if "*" in allowed_tags:
        return pd.DataFrame(data)
    if not tags:
        tags=autoClassify(data, secrets_json)
    if type(data)!=pd.DataFrame:
        new_df=pd.DataFrame(data)
    else:
        new_df=data
    if tags==None or tags==[None] or tags=='OTHER':
        tags=[{}]
    for col_name,tag_name in zip(tags.keys(),tags.values()):
        if tag_name not in allowed_tags and (tag_name !="OTHER" or tag_name!=None):
            new_df[col_name]=pd.NA
    return new_df
