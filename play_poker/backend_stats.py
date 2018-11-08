# odds source: https://en.wikipedia.org/wiki/Poker_probability
from play_poker.poker_controller import get_hand_type


def odds_of_winning(hand):
    # input: a list of cards forming a hand
    # output: probability of winning hand
    hand_type = get_hand_type(hand)

    odds_of_lose = 0
    index = hand_type
    while index <= 9:
        odds_of_lose += odds_of(index)
        index += 1

    hand.sort()
    return (1 - odds_of_lose)*100


def odds_of(hand_type):
    # input: a numerical representation of hand type
    # output: the probability of getting the hand
    if hand_type == 9:
        return 0.0000154
    elif hand_type == 8:
        return 0.0000139
    elif hand_type == 7:
        return 0.00024
    elif hand_type == 6:
        return 0.001441
    elif hand_type == 5:
        return 0.001965
    elif hand_type == 4:
        return 0.003925
    elif hand_type == 3:
        return 0.021128
    elif hand_type == 2:
        return 0.047539
    elif hand_type == 1:
        return 0.422569
    else:
        return 0.5011637
