from rest_framework import serializers
from .models import Movie, Review,Profile,Reaction

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    review=ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 

from rest_framework import serializers
from .models import RecommendedMovie

class RecommendedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedMovie
        fields = '__all__'



class ReactionS(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'