from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load sample data from JSON file
with open('sample_data.json') as f:
    sample_data = json.load(f)

@app.route('/filter_and_paginate', methods=['GET'])
def filter_and_paginate():
    # Get request parameters
    filter_key = request.args.get('filter_key')
    filter_value = request.args.get('filter_value')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    # Filter data based on request parameters
    filtered_data = [item for item in sample_data['data'] if item.get(filter_key) == filter_value]

    # Paginate the filtered data
    total_items = len(filtered_data)
    total_pages = (total_items + page_size - 1) // page_size
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, total_items)
    paginated_data = filtered_data[start_index:end_index]

    # Prepare response
    response = {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "data": paginated_data
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
