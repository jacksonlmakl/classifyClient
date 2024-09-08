from appPostgres import sql
import json

class Account:
    def __init__(self,username,password,account_id,client):
        self.client=client
        self.account_id = self.client.account_id
        if not self.account_id:
            raise Exception("You are not the primary account owner")
        
        
        current_account_dict=sql(f""" 
        SELECT * FROM "DATAPLATFORM"."USERS"."ACCOUNTS" WHERE "ID" = '{self.account_id}' 
        """).to_dict(orient='records')

        if len(current_account_dict)==0:
            raise Exception("You do not have an account associated")
        self.policies_data=json.loads(current_account_dict[0].get("POLICIES_DATA"))
        self.users_data=json.loads(current_account_dict[0].get("USERS_DATA"))
        self.secrets_data=json.loads(current_account_dict[0].get("SECRETS_DATA"))
    def updateSettings(self,key,data):
        if key == 'POLICIES':
            return sql(f"""
            BEGIN;
            UPDATE "USERS"."ACCOUNTS"
            	SET "POLICIES_DATA"= '{json.dumps(data)}'
            	WHERE "ID" = '{self.account_id}';
            COMMIT;
            """)
        elif key == 'USERS':
            return sql(f"""
            BEGIN;
            UPDATE "USERS"."ACCOUNTS"
            	SET  "USERS_DATA"= '{json.dumps(data)}'
            	WHERE "ID" = '{self.account_id}';
            COMMIT;
            """)
        elif key == 'SECRETS':
            return sql(f"""
            BEGIN;
        UPDATE "USERS"."SECRETS"
        	SET "SECRETS_DATA"='{json.dumps(data)}'
        	WHERE "ID" = '{self.account_id}';
        COMMIT;
        """)