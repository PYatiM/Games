class Player:
    def __init__(self):
        self.score = 0

    def decide(self, ai_prediction):
        print(f"\nAI suggests: {ai_prediction.upper()}")
        choice = input("Your action (block/allow): ").strip().lower()
        return choice