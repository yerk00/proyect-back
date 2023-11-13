from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
    new_user = User(username=data['nombre'], password=data['contrasena'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['nombre']).first()
    if not user or not user.password == data['contrasena']:
        return jsonify({'message': 'login failed'})
    return jsonify({'message': 'login successful'})

if __name__ == '__main__':
    app.run(debug=True)

