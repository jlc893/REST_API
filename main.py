from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json

# Creates instance of Flask
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Commands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(100))

    def __repr__(self):
        return f'{self.name} - {self.description}'

@app.route('/')
def render_index():
    return render_template('index.html')

@app.route('/api')
def render_swagger():
    return render_template('swaggerui.html')

@app.route('/api/commands', methods=['GET'])
def get_commands():
    commands = Commands.query.all()
    output = []
    for command in commands:
        command_data = {'id': command.id, 'name': command.name, 'description': command.description}
        output.append(command_data)

    return {"commands": output}


@app.route('/api/commands', methods=['POST'])
def add_command():
    # Get the request data and use it to instantiate a new command
    command = Commands(id=request.json['id'], name=request.json['name'], description=request.json['description'])
    db.session.add(command)
    db.session.commit()
    # Serialize request data into json format
    return jsonify({"id": request.json['id'], "name": request.json['name'], "description": request.json['description']})


@app.route('/api/commands/<id>', methods=['GET'])
def get_command(id):
    command = Commands.query.get(id)
    if command is None:
        return 'Error', 400
    return jsonify({'id': command.id, 'name': command.name, 'description': command.description})


@app.route('/api/commands/<id>', methods=['DELETE'])
def delete_command(id):
    command = Commands.query.get(id)
    if command is None:
        return 'Error', 400
    db.session.delete(command)
    db.session.commit()
    return f'Command {id} has been deleted'

@app.route('/api/commands/<id>', methods=['PUT'])
def update_command(id):
    command = Commands.query.get(id)
    if command is None:
        return {
            "error": "Bad Request",
            "message": "No command found"
        }, 400
    # Unpack the request data and assign it to the command's attributes
    command.name, command.description, command.id = request.json['name'], request.json['description'], request.json['id']
    db.session.commit()
    return jsonify({"id": request.json['id'], "name": request.json['name'], "description": request.json['description']})





if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")