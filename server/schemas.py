#from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    equipment_needed = fields.Bool(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=500))


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=1, max=1000))
    sets = fields.Int(validate=validate.Range(min=1, max=100))
    duration_seconds = fields.Int(validate=validate.Range(min=1, max=86400))

    @validates_schema
    def require_a_measure(self, data, **kwargs):
        """At least one of reps, sets, or duration_seconds must be given."""
        if not any(k in data for k in ('reps', 'sets', 'duration_seconds')):
            raise ValidationError(
                'Provide at least one of reps, sets, or duration_seconds.'
            )


class WorkoutExerciseDetailSchema(WorkoutExerciseSchema):
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseDetailSchema, many=True, dump_only=True)


class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.List(fields.Nested(WorkoutSchema), dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema() schemas go here
