import requests
import pandas as pd
class Connect:
    def __init__(self,email, password):
        self.email = email
        self.password = password

    def table(self,db,schema,tbl):
        # Define the API endpoint and query parameters
        url = 'http://localhost:5555/get_table'
        params = {
            'email': self.email,
            'password': self.password,
            'db': db,
            'schema': schema,
            'tbl': tbl,
            'page': 1
        }
        
        # Make the GET request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return pd.DataFrame(data['data'])
            print("Data:", data['data'])
            print("Pagination Info:", data['pagination'])
        else:
            return response
            print(f"Error: {response.status_code}, {response.text}")
