from rest_framework import serializers
from .models import ExercisesDetails
from exercises.serializers import ExercisesSerializer

class ExercisesDetailsSerializer(serializers.HyperlinkedModelSerializer):
    #exercise_id = serializers.CharField(read_only=True) #use if only want to display exercise name

    #usesexercises serializer for exercise_id to display the exercise assocaited with this details in the JSON.
    exercise_id = ExercisesSerializer(read_only=True)

#    exercise_id = serializers.HyperlinkedRelatedField(
#        view_name='exercises-api-view',
#        lookup_field='exercise',
#        many=True,
#        read_only=True
#    )

    class Meta:
        model = ExercisesDetails
        fields = ['id', 'exercise_id', 'weight', 'set_amount', 'total_reps', 'volume']
   #     extra_kwargs = {
   #         'exercise_id': {'view_name': 'exercises-api-view', 'lookup_field': 'exercise'}
   #     }