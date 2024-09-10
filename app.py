from flask import Flask, request, jsonify
import math
from apiClient import apiClient
import json
from appPostgres import sql
from createUser import createUser
app = Flask(__name__)

@app.route('/get_table', methods=['GET'])
def get_table():
    email = request.args.get('email')
    password = request.args.get('password')
    db = request.args.get('db')
    schema = request.args.get('schema')
    tbl = request.args.get('tbl')
    page = int(request.args.get('page', 1))
    per_page = 100  # Limit to 100 records per page

    # Initialize the apiClient and fetch the table
    c = apiClient(email, password)
    df = c.table(db, schema, tbl)

    # Paginate if necessary
    total_records = len(df)
    total_pages = math.ceil(total_records / per_page)

    if page > total_pages or page < 1:
        return jsonify({"error": "Invalid page number"}), 400

    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_records)
    df_page = df.iloc[start_idx:end_idx]
    
    # Convert to list of dictionaries
    result = df_page.to_dict(orient='records')

    return jsonify({
        "data": result,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_records": total_records,
            "records_per_page": per_page
        }
    })





@app.route('/update_settings', methods=['GET'])
def update_settings():
    email = request.args.get('email')
    password = request.args.get('password')
    
    param_type = request.args.get('param_type')
    data = request.args.get('data')
    print("LOOK: ", email, password)
    client=apiClient(email, password)

    result = client.update_admin_settings(param_type,json.loads(data))
    return jsonify({
        "success": result})


@app.route('/create_user', methods=['GET'])
def create_user():
    email = request.args.get('email')
    pwd = request.args.get('password')
    invite_code = request.args.get('invite_code')
    
    result=createUser(email, pwd, invite_code)
    if result:
        return jsonify({
            "success": True})



@app.route('/get_settings', methods=['GET'])
def get_settings():
    email = request.args.get('email')
    pwd = request.args.get('password')
    query= f""" 
    SELECT "ID","EMAIL","ACCOUNT_ID"
    FROM "USERS"."AUTH"
    WHERE "EMAIL" = '{email}' AND "PASSWORD" = '{pwd}'
    """
    df_user = sql(query)

    account_id=df_user['ACCOUNT_ID'][0]
    user_id=df_user['ID'][0]
    
    acc_query= f""" 
    SELECT 
    "ID",
    "NAME",
    "ADMIN_AUTH_ID",
    "POLICIES_DATA" AS "POLICIES",
    "USERS_DATA" AS "USERS",
    "INVITE_CODE" AS "INVITE_CODE",
    "SECRETS_DATA" AS "SECRETS"
    FROM "USERS"."ACCOUNTS"
    WHERE "ID" = '{account_id}'
    """
    df_account = sql(acc_query)
    try:
        account_admin_user_id=df_account['ADMIN_AUTH_ID'][0]
    except:
        account_admin_user_id=None
        
    if user_id != account_admin_user_id:
        del df_account['INVITE_CODE']
        del df_account['SECRETS']
    user_data = df_user.to_dict(orient='records')
    account_data = df_account.to_dict(orient='records')
    return jsonify({
        "user_settings": user_data,
        "account_settings": account_data })







@app.route('/query', methods=['GET'])
def query():
    email = request.args.get('email')
    password = request.args.get('password')
    
    query = request.args.get('query')
    
    page = int(request.args.get('page', 1))
    per_page = 100  # Limit to 100 records per page

    # Initialize the apiClient and fetch the table
    c = apiClient(email, password)
    df = c.query(query)

    # Paginate if necessary
    total_records = len(df)
    total_pages = math.ceil(total_records / per_page)

    if page > total_pages or page < 1:
        return jsonify({"error": "Invalid page number"}), 400

    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_records)
    df_page = df.iloc[start_idx:end_idx]
    
    # Convert to list of dictionaries
    result = df_page.to_dict(orient='records')

    return jsonify({
        "data": result,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_records": total_records,
            "records_per_page": per_page
        }
    })



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=5555)
