from flask import Flask, request, jsonify
import math
from apiClient import apiClient
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

if __name__ == '__main__':
    app.run(debug=True,port=5555)