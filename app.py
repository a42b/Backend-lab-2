from flask import Flask, request, jsonify
from flask_migrate import Migrate
from config import Config
from models import User, Account, Record
from schemas import AccountSchema, UserSchema, RecordSchema
from extension import db 


# Initialize app and load configuration
app = Flask(__name__)
app.config.from_object(Config)
# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

print(f"Database URI: {Config.SQLALCHEMY_DATABASE_URI}")
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

# User endpoints
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Name field is required'}), 400

    # Create and save a new user
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()

    return UserSchema().dump(new_user), 201


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return UserSchema().dump(user), 200


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return UserSchema(many=True).dump(users), 200

# Record endpoints
@app.route('/record', methods=['POST'])
def create_record():
    data = request.json
    required_fields = ['user_id', 'category_id', 'amount']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if data['amount'] <= 0:
        return jsonify({'error': 'Amount must be positive'}), 400

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Create a new record
    new_record = Record(
        user_id=data['user_id'],
        category_id=data['category_id'],
        amount=data['amount']
    )
    db.session.add(new_record)
    db.session.commit()

    return RecordSchema().dump(new_record), 201


@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = Record.query.get(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404

    return RecordSchema().dump(record), 200


@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = Record.query.get(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'}), 200


@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)

    query = Record.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)

    records = query.all()
    return RecordSchema(many=True).dump(records), 200

# Account endpoints
@app.route('/account/<int:user_id>/add_income', methods=['POST'])
def add_income(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    amount = data.get('amount', 0)

    if amount <= 0:
        return jsonify({'error': 'Invalid amount. Must be a positive number.'}), 400

    # Ensure the account exists and update the balance
    if not user.account:
        user.account = Account(balance=0.0)
    user.account.balance += amount

    db.session.commit()
    return AccountSchema().dump(user.account), 200


@app.route('/account/<int:user_id>', methods=['GET'])
def get_account_balance(user_id):
    user = User.query.get(user_id)
    if not user or not user.account:
        return jsonify({'error': 'Account not found'}), 404

    return AccountSchema().dump(user.account), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
