import os
import json

class ScoreManager:
    def __init__(self):
        self.score_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "puntaje.json")
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0
        self.load_score()

    def save_score(self):
        data = {
            "player_wins": self.player_wins,
            "ai_wins": self.ai_wins,
            "draws": self.draws
        }
        with open(self.score_path, "w") as f:
            json.dump(data, f)

    def load_score(self):
        if os.path.exists(self.score_path):
            try:
                with open(self.score_path, "r") as f:
                    data = json.load(f)
                    self.player_wins = data.get("player_wins", 0)
                    self.ai_wins = data.get("ai_wins", 0)
                    self.draws = data.get("draws", 0)
            except Exception:
                self.player_wins = 0
                self.ai_wins = 0
                self.draws = 0
        else:
            self.player_wins = 0
            self.ai_wins = 0
            self.draws = 0