# simple rule-based ground truth added in gen lab method

import random

class Traffic:
    def __init__(self):
        self.features = self.generate_features()
        self.label = self.generate_label()

    def generate_features(self):
        return {
            "packet_size": random.randint(20, 1500),
            "request_rate": random.randint(1, 100),
            "error_rate": random.random()
        }

    def generate_label(self):
        if self.features["request_rate"] > 70 or self.features["error_rate"] > 0.7:
            return "attack"
        return "normal"