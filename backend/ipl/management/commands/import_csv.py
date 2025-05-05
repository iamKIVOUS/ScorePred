from django.core.management.base import BaseCommand
import csv
from ipl.models import Batter, Bowler, Match
import os

class Command(BaseCommand):
    help = "Import batter, bowler, and match data from CSV files into models"

    def handle(self, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        DATA_DIR = os.path.join(BASE_DIR, '..', '..', 'data')

        # --- Import Batter Data ---
        batter_csv = os.path.join(DATA_DIR, 'batter.csv')
        try:
            with open(batter_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Batter.objects.create(
                        match_id=row["match_id"],
                        player_id=row["player_id"],
                        player_name=row["player_name"],
                        team_id=row["team_id"],
                        batting_position=row["batting_position"],
                        runs_scored=row["runs_scored"],
                        balls_faced=row["balls_faced"],
                        strike_rate=row["strike_rate"],
                        fours=row["fours"],
                        sixes=row["sixes"],
                        how_out=row["how_out"],
                        bolwer_id=row["bolwer_id"]
                    )
            self.stdout.write(self.style.SUCCESS("Batter data imported successfully"))
        except Exception as e:
            self.stderr.write(f"Error importing batter data: {e}")

        # --- Import Bowler Data ---
        bowler_csv = os.path.join(DATA_DIR, 'bowler.csv')
        try:
            with open(bowler_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Bowler.objects.create(
                        match_id=row["match_id"],
                        player_id=row["player_id"],
                        player_name=row["player_name"],
                        team_id=row["team_id"],
                        runs_conceded=row["runs_conceded"],
                        total_overs=row["total_overs"],
                        economy=row["economy"],
                        dots=row["dots"],
                        wickets=row["wickets"],
                        fours=row["fours"],
                        sixes=row["sixes"],
                        wide=row["wide"],
                        no_balls=row["no_balls"]
                    )
            self.stdout.write(self.style.SUCCESS("Bowler data imported successfully"))
        except Exception as e:
            self.stderr.write(f"Error importing bowler data: {e}")

        # --- Import Match Data ---
        match_csv = os.path.join(DATA_DIR, 'match.csv')
        try:
            with open(match_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Match.objects.create(
                        match_id=row["match_id"],
                        date=row["date"],
                        season=row["season"],
                        venue=row["venue"],
                        toss_winner=row["toss_winner"],
                        toss_decision=row["toss_decision"],
                        team_1=row["team_1"],
                        team_2=row["team_2"],
                        team_1_score=row["team_1_score"],
                        team_1_wicket=row["team_1_wicket"],
                        team_2_score=row["team_2_score"],
                        team_2_wicket=row["team_2_wicket"],
                        winner=row["winner"],
                        loser=row["loser"],
                        player_of_the_match=row["player_of_the_match"],
                        umpire_1=row["umpire_1"],
                        umpire_2=row["umpire_2"]
                    )
            self.stdout.write(self.style.SUCCESS("Match data imported successfully"))
        except Exception as e:
            self.stderr.write(f"Error importing match data: {e}")
