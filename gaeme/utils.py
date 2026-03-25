def evaluate(player_action, actual_label):
    if player_action == "block" and actual_label == "attack":
        return True
    if player_action == "allow" and actual_label == "normal":
        return True
    return False