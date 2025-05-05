from rest_framework import serializers
from .models import Team, Player, Match, Prediction

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='team', write_only=True)
    age = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ['id', 'name', 'team', 'team_id', 'position', 'jersey_number', 'height_cm', 'weight_kg', 'age']

    def get_age(self, obj):
        from datetime import date
        return date.today().year - obj.date_of_birth.year


class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    home_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='home_team', write_only=True)
    away_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='away_team', write_only=True)

    class Meta:
        model = Match
        fields = ['id', 'date', 'home_team', 'home_team_id', 'away_team', 'away_team_id', 'home_score', 'away_score']


class PredictionSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)
    match_id = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all(), source='match', write_only=True)

    class Meta:
        model = Prediction
        fields = ['id', 'match', 'match_id', 'predicted_winner', 'confidence', 'created_at']
