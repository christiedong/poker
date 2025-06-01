#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : Tony
# @time    : 2025/6/1 001 16:09
# @function: Poker helper for Tiny Tower Vegas Poker minigame
# @version : V1

import itertools
import sys
from collections import defaultdict
import random

# Scoring rules
SCORE_RULES = {
    'Royal Flush': 5000,
    'Straight Flush': 1500,
    'Four of a Kind': 600,
    'Full House': 300,
    'Flush': 200,
    'Straight': 125,
    'Three of a Kind': 75,
    'Two Pair': 40,
    'Jacks or Better': 10,
    'No Special Hand': 0
}

# Unicode symbols for suits
SUIT_SYMBOLS = {
    'H': '♥',  # Hearts
    'D': '♦',  # Diamonds
    'C': '♣',  # Clubs
    'S': '♠'  # Spades
}


def generate_deck():
    """Generate a standard deck of 52 cards with proper suit symbols"""
    suits = ['H', 'D', 'C', 'S']  # Hearts, Diamonds, Clubs, Spades
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return [suit + value for suit in suits for value in values]


def format_card(card):
    """Format card with proper suit symbol and value"""
    suit = card[0]
    value = card[1:]
    return f"{SUIT_SYMBOLS[suit]}{value}"


def validate_card(card, deck):
    """Validate if a card is in the deck"""
    if len(card) < 2:
        raise ValueError(f"Invalid card: {card}")

    # Handle 10 case
    if card[1:].upper() in ('10', 'T'):
        suit = card[0].upper()
        card = suit + '10'
    else:
        suit = card[0].upper()
        value = card[1].upper()
        card = suit + value

    if card not in deck:
        raise ValueError(f"Invalid card: {card}")
    return card


def parse_hand_input(input_cards, deck):
    """Parse command line input into valid card list"""
    hand = []
    for card in input_cards:
        hand.append(validate_card(card, deck))
    return hand


def is_straight(values):
    """Check if the values form a straight"""
    value_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    unique_values = sorted(set(values), key=lambda x: value_order.index(x))

    # Check for regular straight
    for i in range(len(unique_values) - 4):
        if (value_order.index(unique_values[i + 4]) - value_order.index(unique_values[i])) == 4:
            return True

    # Special case for Ace-low straight (A-2-3-4-5)
    if set(values) >= {'A', '2', '3', '4', '5'}:
        return True

    return False


def analyze_hand(hand):
    """Determine the strongest hand type from given cards"""
    values = [card[1:] for card in hand]  # Handle '10' correctly
    suits = [card[0] for card in hand]

    # Count occurrences of each value and suit
    value_counts = defaultdict(int)
    for v in values:
        value_counts[v] += 1

    suit_counts = defaultdict(int)
    for s in suits:
        suit_counts[s] += 1

    # Check for flush and straight first
    is_fl = len(set(suits)) == 1  # Flush
    is_str = is_straight(values)  # Straight

    # Check for royal flush
    if is_fl and {'10', 'J', 'Q', 'K', 'A'} == set(values):
        return 'Royal Flush'

    # Check for straight flush
    if is_fl and is_str:
        return 'Straight Flush'

    # Check four of a kind
    if any(cnt == 4 for cnt in value_counts.values()):
        return 'Four of a Kind'

    # Check full house
    if sorted(value_counts.values()) == [2, 3]:
        return 'Full House'

    # Check flush
    if is_fl:
        return 'Flush'

    # Check straight
    if is_str:
        return 'Straight'

    # Check three of a kind
    if any(cnt == 3 for cnt in value_counts.values()):
        return 'Three of a Kind'

    # Check two pair
    if list(value_counts.values()).count(2) >= 2:
        return 'Two Pair'

    # Check jacks or better
    if any(cnt == 2 and v in {'J', 'Q', 'K', 'A'} for v, cnt in value_counts.items()):
        return 'Jacks or Better'

    return 'No Special Hand'


def exact_expected_score(deck, hand, kept_cards):
    """Calculate exact expected score by enumerating all possible draws"""
    remaining_deck = [card for card in deck if card not in hand]
    num_to_draw = 5 - len(kept_cards)

    # If holding all cards, just score the current hand
    if num_to_draw == 0:
        hand_type = analyze_hand(kept_cards)
        return SCORE_RULES[hand_type]

    total_score = 0
    total_possibilities = 0

    # Enumerate all possible ways to draw replacement cards
    for drawn_cards in itertools.combinations(remaining_deck, num_to_draw):
        current_hand = kept_cards + list(drawn_cards)
        hand_type = analyze_hand(current_hand)
        total_score += SCORE_RULES[hand_type]
        total_possibilities += 1

    return round(total_score / total_possibilities, 2) if total_possibilities > 0 else 0


def find_best_hold(hand, deck):
    """Find the optimal cards to hold for maximum expected score"""
    best_hold = None
    best_score = -1
    results = []

    # Evaluate all possible holding strategies (keeping 0-3 or all 5 cards)
    for keep in range(0, 6):
        # Skip holding 4 cards as per game rules
        # if keep == 4:
        #     continue

        for kept_cards in itertools.combinations(hand, keep):
            expected_score = exact_expected_score(deck, hand, list(kept_cards))
            results.append((kept_cards, expected_score))

            if expected_score > best_score:
                best_score = expected_score
                best_hold = kept_cards

    # Organize results by number of cards held
    results_by_keep = defaultdict(list)
    for kept_cards, score in results:
        results_by_keep[len(kept_cards)].append((kept_cards, score))

    # Print analysis table
    print("\nHolding Strategy Analysis:")
    print("{:<30} {:<15} {:<15}".format("Cards Held", "Expected Score", "Possibilities"))
    print("-" * 65)

    for keep_num in sorted(results_by_keep.keys()):
        for kept_cards, score in sorted(results_by_keep[keep_num], key=lambda x: -x[1]):
            # Format cards with symbols
            cards_str = " ".join([format_card(c) for c in kept_cards]) if kept_cards else "None"
            possibilities = len(list(itertools.combinations(
                [card for card in deck if card not in hand],
                5 - len(kept_cards))
            ))
            print("{:<30} {:<15.2f} {:<15,}".format(cards_str, score, possibilities))

    return best_hold, best_score


def main():
    # Initialize deck
    deck = generate_deck()

    # Handle command line arguments
    if len(sys.argv) > 1:
        try:
            hand = parse_hand_input(sys.argv[1:], deck)
            if len(hand) != 5:
                raise ValueError("Exactly 5 cards must be specified")
        except ValueError as e:
            print(f"Error: {e}")
            print("Usage: python poker.py [card1 card2 card3 card4 card5]")
            print("Example: python poker.py HA D10 CQ SK S2")
            print("Card format: [H|D|C|S][A|2-10|J|Q|K]")
            print("H=♥ D=♦ C=♣ S=♠")
            sys.exit(1)
    else:
        # Random hand if no arguments provided
        hand = random.sample(deck, 5)

    # Display initial hand with symbols
    print("Initial Hand:", " ".join([format_card(c) for c in hand]))

    # Analyze initial hand
    initial_type = analyze_hand(hand)
    initial_score = SCORE_RULES[initial_type]
    print("Initial Hand Type:", initial_type, "Score:", initial_score)

    # Find optimal holding strategy
    best_hold, best_score = find_best_hold(hand, deck)

    # Display optimal strategy
    print("\nOptimal Strategy:")
    print("Cards to Hold:", " ".join([format_card(c) for c in best_hold]) if best_hold else "None")
    print("Expected Score:", best_score)

    # Compare with initial score
    improvement = best_score - initial_score
    if improvement > 0:
        print("Score Improvement Over Keeping All:", improvement)
    else:
        print("Recommend Keeping All Cards")


if __name__ == "__main__":
    # random.seed(42)  # Uncomment for reproducible results
    main()
