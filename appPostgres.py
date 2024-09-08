import pandas as pd
import numpy as np
from sqlalchemy import create_engine,text
import psycopg2
from getAppSecret import getAppSecret
def pg_connection():
    
    # PostgreSQL connection details
    username = getAppSecret('db_username')
    password = getAppSecret('db_password')
    host = getAppSecret('db_host')
    port = getAppSecret('db_port')
    database = getAppSecret('db_database')
    
    # Create connection string
    connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
    
    conn=create_engine(connection_string).connect()
    return conn
    
def sql(query):
    # Example of executing a SQL query to create a new table
    conn=pg_connection()
    r=conn.execute(text(query))
    if r.returns_rows:
        keys=list(r.keys())
        rows=r.all()
        data=[dict(zip(keys,i)) for i in rows]
        conn.close()
        return pd.DataFrame(data)
    else:
        conn.close()
        return r


def df_to_table(df,schema,table_name):

    # Create engine
    engine = pg_connection().engine
    
    # Write the DataFrame to PostgreSQL, specifying the schema
    df.to_sql(table_name, engine, schema=schema, if_exists='append', index=False)
    
    print("Data successfully written to the ANALYSIS schema in PostgreSQL")
    return df