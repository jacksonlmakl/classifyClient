from appPostgres import *
from createToken import *
import hashlib
def hashmd5(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    hash_md5 = md5_hash.hexdigest()
    return hash_md5
def createUser(email, pwd, invite_code):
    user_id=hashmd5(email)
    token=generate_token(email)

    q=f""" SELECT "ID" AS "ID" FROM "USERS"."ACCOUNTS" WHERE "INVITE_CODE"='{invite_code}' """
    account_id=list(sql(q)["ID"])[0] if len(list(sql(q)["ID"])) >0 else None

    if not account_id:
        return "Invalid Invite Code"

    q2=f""" SELECT "EMAIL" AS "EMAIL" FROM "USERS"."AUTH" """
    emails=list(sql(q2)["EMAIL"])
    if email in emails:
        return "Email already exists"

    else:
        insert_q=f"""
        BEGIN;
        INSERT INTO "USERS"."AUTH"(
        	"ID", "EMAIL", "PASSWORD", "TOKEN", "ACCOUNT_ID")
        	VALUES ('{user_id}', '{email}', '{pwd}', '{token}', '{account_id}');
        COMMIT;
        """
        sql(insert_q)
    return token