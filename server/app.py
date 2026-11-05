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
# ---------- Workouts ----------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    return make_response(jsonify(workout_detail_schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json(silent=True) or {})
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 400)
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return make_response(jsonify({'errors': str(err)}), 400)
    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    db.session.delete(workout)   # cascade removes its WorkoutExercises
    db.session.commit()
    return make_response('', 204)


# ---------- Exercises ----------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    return make_response(jsonify(exercise_detail_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json(silent=True) or {})
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 400)
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return make_response(jsonify({'errors': str(err)}), 400)
    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    db.session.delete(exercise)  # cascade removes its WorkoutExercises
    db.session.commit()
    return make_response('', 204)


# ---------- Add an exercise to a workout ----------

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST'],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return make_response(jsonify({'error': 'Workout or Exercise not found'}), 404)

    try:
        data = workout_exercise_schema.load(request.get_json(silent=True) or {})
        we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
        db.session.add(we)
        db.session.commit()
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 400)
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return make_response(jsonify({'errors': str(err)}), 400)
    return make_response(jsonify(workout_exercise_schema.dump(we)), 201)
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