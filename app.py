from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/example'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, name='nombre')
    password = db.Column(db.String(100), nullable=False, name='contrasena')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['contrasena'])
    new_user = User(username=data['nombre'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['nombre']).first()
    if not user or not check_password_hash(user.password, data['contrasena']):
        return jsonify({'message': 'login failed'})
    return jsonify({'message': 'login successful'})


if __name__ == '__main__':
    app.run(debug=True)

