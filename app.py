from flask import Flask, request, jsonify
from models import users, categories, records, user_id_counter, category_id_counter, record_id_counter
from datetime import datetime

app = Flask(__name__)

# Global Error Handlers
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# Helper function to validate required fields
def validate_json(required_fields, data):
    if not data:
        return {'error': 'Request body is missing'}, 400

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {'error': f"Missing fields: {', '.join(missing_fields)}"}, 400
    return None


# User endpoints
@app.route('/user', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.json

    # Validate input
    validation_error = validate_json(['name'], data)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    user_id = user_id_counter
    users[user_id] = {'id': user_id, 'name': data['name']}
    user_id_counter += 1
    return jsonify(users[user_id]), 201


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({'message': 'User deleted'})
    return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200


# Category endpoints
@app.route('/category', methods=['POST'])
def create_category():
    global category_id_counter
    data = request.json

    # Validate input
    validation_error = validate_json(['name'], data)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    category_id = category_id_counter
    categories[category_id] = {'id': category_id, 'name': data['name']}
    category_id_counter += 1
    return jsonify(categories[category_id]), 201


@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values())), 200


@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id in categories:
        del categories[category_id]
        return jsonify({'message': 'Category deleted'})
    return jsonify({'error': 'Category not found'}), 404


# Record endpoints
@app.route('/record', methods=['POST'])
def create_record():
    global record_id_counter
    data = request.json

    # Validate input
    validation_error = validate_json(['user_id', 'category_id', 'amount'], data)
    if validation_error:
        return jsonify(validation_error[0]), validation_error[1]

    if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        return jsonify({'error': 'Amount must be a positive number'}), 400

    if data['user_id'] not in users:
        return jsonify({'error': 'User ID not found'}), 404

    if data['category_id'] not in categories:
        return jsonify({'error': 'Category ID not found'}), 404

    record_id = record_id_counter
    record = {
        'id': record_id,
        'user_id': data['user_id'],
        'category_id': data['category_id'],
        'amount': data['amount'],
        'timestamp': datetime.now().isoformat()
    }
    records[record_id] = record
    record_id_counter += 1
    return jsonify(record), 201


@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = records.get(record_id)
    if record:
        return jsonify(record)
    return jsonify({'error': 'Record not found'}), 404


@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in records:
        del records[record_id]
        return jsonify({'message': 'Record deleted'})
    return jsonify({'error': 'Record not found'}), 404


@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)

    if user_id is None and category_id is None:
        return jsonify({'error': 'Specify user_id or category_id'}), 400

    filtered_records = [
        record for record in records.values()
        if (user_id is None or record['user_id'] == user_id) and
           (category_id is None or record['category_id'] == category_id)
    ]
    return jsonify(filtered_records), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
