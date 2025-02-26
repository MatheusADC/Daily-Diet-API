from flask import Flask, request, jsonify
from models.diet import Diet
from database import db
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = "YOUR_KEY"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///YOUR_DATABASE.db'

db.init_app(app)

# Create Diet
@app.route('/create', methods=['POST'])
def create_diet():
    data = request.get_json()

    # Date Handling
    try:
        date_str = data.get('date')
        date_obj = datetime.fromisoformat(date_str.replace("Z", ""))
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)'}), 400

    new_diet = Diet(
        name=data.get('name'),
        description=data.get('description'),
        date=date_obj,
        inside_diet=data.get('inside_diet')
    )
    db.session.add(new_diet)
    db.session.commit()
    return jsonify({'message': 'Diet created successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)