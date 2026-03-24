import random
from collections import Counter

# Card setup
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10',
         'J', 'Q', 'K', 'A']

# Create deck
def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

# Card value mapping
value_map = {r: i for i, r in enumerate(ranks, start=2)}

# Deal cards
def deal(deck, n):
    return [deck.pop() for _ in range(n)]

# Evaluate hand (basic ranking)
def evaluate_hand(cards):
    values = sorted([value_map[c[0]] for c in cards], reverse=True)
    suits_list = [c[1] for c in cards]

    value_counts = Counter(values)
    counts = sorted(value_counts.values(), reverse=True)

    is_flush = len(set(suits_list)) == 1
    is_straight = len(set(values)) == 5 and max(values) - min(values) == 4

    if is_straight and is_flush:
        return (8, max(values))  # Straight flush
    elif 4 in counts:
        return (7, max(values))  # Four of a kind
    elif 3 in counts and 2 in counts:
        return (6, max(values))  # Full house
    elif is_flush:
        return (5, max(values))
    elif is_straight:
        return (4, max(values))
    elif 3 in counts:
        return (3, max(values))
    elif counts.count(2) == 2:
        return (2, max(values))  # Two pair
    elif 2 in counts:
        return (1, max(values))  # One pair
    else:
        return (0, max(values))  # High card

# Get best 5-card combination from 7 cards
from itertools import combinations
def best_hand(seven_cards):
    return max(evaluate_hand(list(combo)) for combo in combinations(seven_cards, 5))

# Game flow
def play():
    deck = create_deck()
    random.shuffle(deck)

    player = deal(deck, 2)
    dealer = deal(deck, 2)

    flop = deal(deck, 3)
    turn = deal(deck, 1)
    river = deal(deck, 1)

    community = flop + turn + river

    print("Your Cards:", player)
    print("Dealer Cards:", dealer)
    print("Community Cards:", community)

    player_score = best_hand(player + community)
    dealer_score = best_hand(dealer + community)

    print("Your Score:", player_score)
    print("Dealer Score:", dealer_score)

    if player_score > dealer_score:
        print("You win!")
    elif player_score < dealer_score:
        print("Dealer wins!")
    else:
        print("It's a tie!")

# Run game
if __name__ == "__main__":
    play()
