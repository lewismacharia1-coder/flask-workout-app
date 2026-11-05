from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing tables...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Seeding exercises...')
    squat = Exercise(name='Squat', category='Strength', equipment_needed=True)
    pushup = Exercise(name='Push-up', category='Strength', equipment_needed=False)
    plank = Exercise(name='Plank', category='Core', equipment_needed=False)
    run = Exercise(name='Running', category='Cardio', equipment_needed=False)
    db.session.add_all([squat, pushup, plank, run])
    db.session.commit()

    print('Seeding workouts...')
    w1 = Workout(date=date(2026, 11, 1), duration_minutes=45, notes='Leg day')
    w2 = Workout(date=date(2026, 11, 3), duration_minutes=30, notes='Quick core and cardio')
    w3 = Workout(date=date(2026, 11, 5), duration_minutes=60, notes='Full body')
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    print('Linking exercises to workouts...')
    links = [
        WorkoutExercise(workout_id=w1.id, exercise_id=squat.id, reps=10, sets=4),
        WorkoutExercise(workout_id=w1.id, exercise_id=run.id, duration_seconds=600),
        WorkoutExercise(workout_id=w2.id, exercise_id=plank.id, sets=3, duration_seconds=60),
        WorkoutExercise(workout_id=w2.id, exercise_id=run.id, duration_seconds=900),
        WorkoutExercise(workout_id=w3.id, exercise_id=pushup.id, reps=15, sets=3),
        WorkoutExercise(workout_id=w3.id, exercise_id=squat.id, reps=8, sets=5),
    ]
    db.session.add_all(links)
    db.session.commit()

    print('Done seeding!')