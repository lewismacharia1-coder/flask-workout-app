import os

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import *
from schemas import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return WorkoutSchema(many=True).dump(workouts), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {'error': 'Workout not found'}, 404
    return WorkoutSchema().dump(workout), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        workout = WorkoutSchema().load(request.get_json(), session=db.session)
        db.session.add(workout)
        db.session.commit()
        return WorkoutSchema().dump(workout), 201
    except ValidationError as e:
        return {'errors': e.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Could not create workout'}, 422


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return {'error': 'Workout not found'}, 404
    db.session.delete(workout)
    db.session.commit()
    return {}, 204


@app.route('/exercises', methods=['GET'])
def get_exercises():
    return ExerciseSchema(many=True).dump(Exercise.query.all()), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return {'error': 'Exercise not found'}, 404
    return ExerciseSchema().dump(exercise), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)