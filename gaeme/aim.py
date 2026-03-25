import random

class SimpleAI:
    def predict(self, traffic):
        f = traffic.features

        # imperfect AI (simulates ML errors)
        if f["request_rate"] > 60 or f["error_rate"] > 0.6:
            prediction = "attack"
        else:
            prediction = "normal"

        # introduce noise (AI not perfect)
        if random.random() < 0.1:
            prediction = "attack" if prediction == "normal" else "normal"

        return prediction