import os
import joblib
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Team, Player, Match, Prediction
from .serializers import TeamSerializer, PlayerSerializer, MatchSerializer, PredictionSerializer

# ---------------- Model Loading ------------------
MODEL_VERSION = "v1"
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_model', f'model_{MODEL_VERSION}.pkl')

try:
    model = joblib.load(MODEL_PATH)
    print(f"[ML] Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    model = None
    print(f"[ML] Model file not found at {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"[ML] Error loading model: {e}")

# ---------------- ViewSets ------------------

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

# ---------------- Prediction API ------------------

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache prediction for 15 minutes
class PredictOutcomeView(APIView):
    def post(self, request):
        match_id = request.data.get('match_id')

        try:
            match = Match.objects.get(id=match_id)

            if not model:
                return Response({'error': 'ML model not loaded.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # TODO: Replace with actual feature extraction from match/team/player stats
            # Replace the dummy features with actual data related to the match
            features = [match.home_score, match.away_score]  # Example features based on match scores

            prediction_probs = model.predict_proba([features])[0]
            predicted_class = model.predict([features])[0]

            predicted_team = match.team_home if predicted_class == 0 else match.team_away

            prediction = Prediction.objects.create(
                match=match,
                predicted_winner=predicted_team,
                probability_home_win=prediction_probs[0],
                probability_away_win=prediction_probs[1],
                confidence=max(prediction_probs),  # Store the max probability as confidence
                model_version=MODEL_VERSION
            )

            serializer = PredictionSerializer(prediction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Match.DoesNotExist:
            return Response({'error': 'Match not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
