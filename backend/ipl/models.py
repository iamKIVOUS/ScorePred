from django.db import models

class Batter(models.Model):
    match_id = models.CharField(max_length=50)
    player_id = models.CharField(max_length=50)
    player_name = models.CharField(max_length=100)
    team_id = models.CharField(max_length=50)
    batting_position = models.IntegerField()
    runs_scored = models.IntegerField()
    balls_faced = models.IntegerField()
    strike_rate = models.FloatField()
    fours = models.IntegerField()
    sixes = models.IntegerField()
    how_out = models.CharField(max_length=100)
    bowler_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.player_name} ({self.match_id})"

class Bowler(models.Model):
    match_id = models.CharField(max_length=50)
    player_id = models.CharField(max_length=50)
    player_name = models.CharField(max_length=100)
    team_id = models.CharField(max_length=50)
    runs_conceded = models.IntegerField()
    total_overs = models.FloatField()
    economy = models.FloatField()
    dots = models.IntegerField()
    wickets = models.IntegerField()
    fours = models.IntegerField()
    sixes = models.IntegerField()
    wide = models.IntegerField()
    no_balls = models.IntegerField()

    def __str__(self):
        return f"{self.player_name} ({self.match_id})"

class Match(models.Model):
    match_id = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    season = models.IntegerField()
    venue = models.CharField(max_length=100)
    toss_winner = models.CharField(max_length=100)
    toss_decision = models.CharField(max_length=10)
    team_1 = models.CharField(max_length=100)
    team_2 = models.CharField(max_length=100)
    team_1_score = models.IntegerField()
    team_1_wicket = models.IntegerField()
    team_2_score = models.IntegerField()
    team_2_wicket = models.IntegerField()
    winner = models.CharField(max_length=100)
    loser = models.CharField(max_length=100)
    player_of_the_match = models.CharField(max_length=100)
    umpire_1 = models.CharField(max_length=100)
    umpire_2 = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.match_id} - {self.team_1} vs {self.team_2}"
