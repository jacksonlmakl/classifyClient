from appPostgres import *
from createToken import generate_token

def login(email,password):
    q=f""" 
    SELECT * FROM "USERS"."AUTH" 
    WHERE "EMAIL" = '{email}' AND "PASSWORD" = '{password}' 
    """
    r=sql(q)

    if len(r) < 1:
        return False
    
    new_token=generate_token(email)
    update_q=f""" 
    BEGIN;
    UPDATE "USERS"."AUTH"
    	SET "TOKEN"='{new_token}'
    	WHERE "EMAIL"='{email}';
    COMMIT;
    """
    sql(update_q)
    return {"token":new_token, "email":email}