#sample ai with noise and imperfection added in predict method to simulate more accurate outputs
import random

class SimpleAI:
    def predict(self, traffic):
        f = traffic.features

        if f["request_rate"] > 60 or f["error_rate"] > 0.6:
            prediction = "attack"
        else:
            prediction = "normal"

        if random.random() < 0.1:
            prediction = "attack" if prediction == "normal" else "normal"

        return prediction