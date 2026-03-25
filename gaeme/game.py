from aim import SimpleAI
from traffic import Traffic
from play import Player
from utils import evaluate
import config

class CyberGame:
    def __init__(self):
        self.ai = SimpleAI()
        self.player = Player()
        self.rounds = config.ROUNDS

    def play_round(self, round_num):
        print(f"\n=== Round {round_num} ===")

        traffic = Traffic()
        print("Traffic Features:", traffic.features)

        ai_pred = self.ai.predict(traffic)
        action = self.player.decide(ai_pred)

        correct = evaluate(action, traffic.label)

        if correct:
            print("✔ Correct decision")
            self.player.score += 1
        else:
            print("✘ Wrong decision - System compromised!")

        print("Actual:", traffic.label)

    def run(self):
        for i in range(1, self.rounds + 1):
            self.play_round(i)

        print("\nFinal Score:", self.player.score)