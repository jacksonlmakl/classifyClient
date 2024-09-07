import pandas as pd
import numpy as np
from sqlalchemy import create_engine,text
import psycopg2
from CORE.getSecrets import getSecret
def pg_connection(secrets_json={}):
    
    # PostgreSQL connection details
    username = getSecret('db_username',secrets_json)
    password = getSecret('db_password',secrets_json)
    host = getSecret('db_host',secrets_json)
    port = getSecret('db_port',secrets_json)
    database = getSecret('db_database',secrets_json)
    
    # Create connection string
    connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
    
    conn=create_engine(connection_string).connect()
    return conn
    
def sql(query, secrets_json={}):
    # Example of executing a SQL query to create a new table
    
    conn=pg_connection(secrets_json)
    r=conn.execute(text(query))
    if r.returns_rows:
        keys=list(r.keys())
        rows=r.all()
        data=[dict(zip(keys,i)) for i in rows]
        return pd.DataFrame(data)
    else:
        return r


def df_to_table(df,schema,table_name):

    # Create engine
    engine = pg_connection().engine
    
    # Write the DataFrame to PostgreSQL, specifying the schema
    df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)
    
    print("Data successfully written to the ANALYSIS schema in PostgreSQL")
    return df