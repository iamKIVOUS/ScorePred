# backend/basketball/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, PlayerViewSet, MatchViewSet, PredictionViewSet, PredictOutcomeView
from rest_framework.authtoken.views import obtain_auth_token

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'predictions', PredictionViewSet)

# Define the urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include all router-generated URLs
    path('predict/', PredictOutcomeView.as_view(), name='predict'),  # Prediction endpoint
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Token authentication endpoint
]
