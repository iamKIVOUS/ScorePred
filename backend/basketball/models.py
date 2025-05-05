from django.db import models
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    coach_name = models.CharField(max_length=100)
    founded_year = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Player(models.Model):
    POSITION_CHOICES = [
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center'),
    ]

    name = models.CharField(max_length=100)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='players',
        db_index=True
    )
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    jersey_number = models.PositiveIntegerField()
    height_cm = models.PositiveIntegerField()
    weight_kg = models.PositiveIntegerField()
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.team.name})"


class Match(models.Model):
    date = models.DateField(db_index=True)
    location = models.CharField(max_length=100)
    team_home = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='home_matches'
    )
    team_away = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='away_matches'
    )
    final_score_home = models.PositiveIntegerField(null=True, blank=True)
    final_score_away = models.PositiveIntegerField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # For prediction feature extraction
    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.team_home.name} vs {self.team_away.name} on {self.date}"


class PlayerPerformance(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='performances',
        db_index=True
    )
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='player_performances',
        db_index=True
    )
    minutes_played = models.FloatField()
    points = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    rebounds = models.PositiveIntegerField()
    steals = models.PositiveIntegerField()
    blocks = models.PositiveIntegerField()
    turnovers = models.PositiveIntegerField()

    class Meta:
        unique_together = ('player', 'match')
        verbose_name = "Player Performance"
        verbose_name_plural = "Player Performances"

    def __str__(self):
        return f"{self.player.name} in {self.match}"


class Prediction(models.Model):
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name='prediction'
    )
    predicted_winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='predicted_wins'
    )
    probability_home_win = models.FloatField(null=True, blank=True)
    probability_away_win = models.FloatField(null=True, blank=True)
    model_version = models.CharField(max_length=20, default='v1')
    confidence = models.FloatField(null=True, blank=True)  # Add confidence field for predictions
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.match}"

