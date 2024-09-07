import os
from CORE.userDataFrame import userDataFrame
from CORE.postgres import sql

class Client:
    def __init__(self,email,policies_json, users_json, secrets_json):
        self.email = email
        self.secrets_json= secrets_json
        self.policies_json=policies_json
        self.users_json=users_json
    def table(self,database_name,schema_name,table_name, policies_json, users_json, secrets_json):
        df= sql(f"""select * from "{database_name}"."{schema_name}"."{table_name}" """, secrets_json)
        return userDataFrame(self.email,df,policies_json, users_json, secrets_json)
    