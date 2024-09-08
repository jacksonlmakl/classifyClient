from login import login
from appPostgres import *
import json
from CORE.Client import Client
from Account import Account
class apiClient:
    def __init__(self, email,password):
        x=login(email,password)
        token=x['token']
        self.email=email
        self.password=password
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
        auth_acc_query=f"""
        SELECT AUTH."ID" AS AUTH_ID,AUTH."EMAIL",ACC."ID" as "ACC_ID"
                FROM "USERS"."ACCOUNTS" ACC 
                LEFT JOIN "USERS"."AUTH" AUTH
                ON ACC."ADMIN_AUTH_ID" = AUTH."ID"
        		WHERE "TOKEN" = '{token}'
        """
        auth_acc_df = sql(auth_acc_query)

        self.is_account_owner = True if len(auth_acc_df)>0 else False
        if self.is_account_owner:
            self.account_id=list(auth_acc_df['ACC_ID'])[0]
        else:
            self.account_id=None
    def table(self,database_name,schema_name,table_name):
        df = self.client.table(database_name,schema_name,table_name, self.policies_json, self.users_json, self.secrets_json)
        return df
    def update_admin_settings(self,param_type,data):
        if self.account_id:
            a=Account(self.email,self.password,self.account_id,self)
            a.updateSettings(param_type,data)
            return True
        else:
            raise Exception("You are not an account admin")
        
        