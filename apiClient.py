from login import login
from appPostgres import *
import json
from CORE.Client import Client

class apiClient:
    def __init__(self, email,password):
        x=login(email,password)
        token=x['token']
        r=sql(f''' SELECT ACC."ID" as "ACC_ID"
        FROM "USERS"."ACCOUNTS" ACC 
        LEFT JOIN "USERS"."AUTH" AUTH
        ON ACC."ID" = AUTH."ACCOUNT_ID"
        WHERE AUTH."TOKEN" = '{token}' ''')
        if len(r)<1:
            return False
        acc_id = list(r['ACC_ID'])[0]
        # acc_id='1'
        accounts=sql(f'''SELECT * FROM "USERS"."ACCOUNTS" WHERE "ID"='{acc_id}' ''')
        
        self.policies_json =  json.loads(list(accounts['POLICIES_DATA'])[0])
        self.users_json =  json.loads(list(accounts['USERS_DATA'])[0])
        self.secrets_json= json.loads(list(accounts['SECRETS_DATA'])[0])
        
    
        self.client= Client(email,self.policies_json, self.users_json, self.secrets_json)

    def table(self,database_name,schema_name,table_name):
        df = self.client.table(database_name,schema_name,table_name, self.policies_json, self.users_json, self.secrets_json)
        return df
        