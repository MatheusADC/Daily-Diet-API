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
        return jsonify({'message': 'Invalid date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)'}), 400

    new_diet = Diet(
        name=data.get('name'),
        description=data.get('description'),
        date=date_obj,
        inside_diet=data.get('inside_diet')
    )
    db.session.add(new_diet)
    db.session.commit()
    return jsonify({'message': 'Diet created successfully!'}), 201

@app.route('/read', methods=['GET'])
def read_all_diets():
    diets = Diet.query.all()
    return jsonify([
        {
            "name": diet.name, 
            "description": diet.description, 
            "date": diet.date, 
            "inside_diet": diet.inside_diet
        }
        
        for diet in diets
    ])


@app.route('/read/<int:id_diet>', methods=['GET'])
def read_diet(id_diet):
    diet = Diet.query.get(id_diet)
    if diet:
        return {"name": diet.name, "description": diet.description, "date": diet.date, "inside_diet": diet.inside_diet}
    return jsonify({'message': 'Diet not found'}), 404

@app.route('/update/<int:id_diet>', methods=['PUT'])
def update_diet(id_diet):
    data = request.get_json()
    diet = Diet.query.get(id_diet)
    if diet:
        diet.name = data.get('name', diet.name)
        diet.description = data.get('description', diet.description)
        diet.date = data.get('date', diet.date)
        diet.inside_diet = data.get('inside_diet', diet.inside_diet)
        db.session.commit()
        return jsonify({'message': f'Diet {id_diet} was updated successfully!'})
    return jsonify({'message': 'Diet not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)