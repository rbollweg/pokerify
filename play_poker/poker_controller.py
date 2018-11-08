# Python program to shuffle a deck of card using the module random and draw 5 cards

# import modules
import itertools, random

from copy import deepcopy


class PokerGame:
    player_scores = []
    deck = []
    rounds = []

    @staticmethod
    def create_deck():
        # make a deck of cards
        deck = list(itertools.product(range(2, 14), ['Spades', 'Hearts', 'Diamonds', 'Clubs']))
        # shuffle the cards
        random.shuffle(deck)
        for index, card in enumerate(deck):
            deck[index] = Card(card[0], card[1])  # replace with our card object
        return deck


class Round:
    player_hands = []
    player_actions = []
    winners = []
    is_tie = False

    def __init__(self, remaining_deck, num_players):
        self.player_hands = self.deal_hands(remaining_deck, num_players)

    @staticmethod
    def deal_hands(deck, num_players):
        # draw five cards
        print('Dealing Hands')
        player_hands = []
        for pl in range(num_players):
            hand = []
            for i in range(0, 5):
                print("Dealt " + str(deck[i].value) + " of " + deck[i].suit + "- Player " + str(pl))
                hand.append(deck.pop(0))
            player_hands.append(hand)
        return player_hands


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        return self.value < other.value


def sort_hand(hand):  # sort a hand by descending value, suit is not taken into account
    hand.sort(reverse=True)
    return hand


def is_straight(hand, i):
    if i == len(hand)-1:
        return True # we are at the end of the hand array, return true
    elif hand[i].value == hand[i + 1].value + 1:  # look at the next card and see it is +1 of the previous card
        return is_straight(hand, i + 1)
    else:
        return False


def is_flush(hand):
    card_suits = [card.suit for card in hand]
    return all(card_suit == card_suits[0] for card_suit in card_suits)


def get_max_value(hand):  # as the hand is sorted, in theory the 0 index is the highest value
    return hand[0].value


def get_num_repetitions(hand):
    hand_copy = deepcopy(hand)
    card_values = [card.value for card in hand_copy]
    print('Card Values: ' + str(card_values))
    max_repetitions = 1
    for value in card_values:
        repetitions = card_values.count(value)
        hand_copy = [card for card in hand_copy if
                     card.value != value]  # maybe not the best way to do this, as we create a new list every time
        if repetitions != 1:  # if we have a repetition
            max_repetitions = repetitions
            second_run = get_num_repetitions(hand_copy)  # redo this function with the truncated list
            if second_run == 1:  # if we do not have a second repetition, just return the first find
                return max_repetitions
            else:  # if not, then return both the repetitions as a list (this means two pair, or a full house)
                repetitions_list = [max_repetitions, second_run]
                return sorted(repetitions_list, reverse=True)
    return max_repetitions  # if we get through every iteration, this should always return 1


def get_hand_type(hand):
    # input: a list of cards forming a hand
    # output: a numerical representation of hand type
    hand = sort_hand(hand)
    print('Hand is: ')
    for card in hand:
        print(str(card.value) + ' of ' + card.suit)
    is_hand_flush = is_flush(hand)
    print('Hand is Flush: ' + str(is_hand_flush))
    is_hand_straight = is_straight(hand, 0)
    print('Hand is Straight: ' + str(is_hand_straight))
    hand_num_reptitions = get_num_repetitions(hand)
    print('Hand number of Repetitions: ' + str(hand_num_reptitions))
    hand_max_value = get_max_value(hand)
    print('Max Value: ' + str(hand_max_value))

    if is_hand_flush and is_hand_straight and hand_max_value == 14:  # royal flush
        return 9
    elif is_hand_straight and is_hand_flush:  # straight flush
        return 8
    elif hand_num_reptitions == 4:  # four of a kind
        return 7
    elif hand_num_reptitions == [3, 2]:  # full house
        return 6
    elif is_hand_flush:  # flush
        return 5
    elif is_hand_straight:  # straight
        return 4
    elif hand_num_reptitions == 3:  # three of a kind
        return 3
    elif hand_num_reptitions == [2, 2]:  # two pair
        return 2
    elif hand_num_reptitions == 2:  # one pair
        return 1
    else:
        return 0  # card high, needs to be fixed


def get_duplicate_values(hand):
    #  output: [[number of repetitions, value], [second number of repetitions, value]]
    hand_copy = deepcopy(hand)
    card_values = [card.value for card in hand_copy]
    print('Card Values: ' + str(card_values))
    max_repetitions = 1
    repetition_value = 0
    for value in card_values:
        repetitions = card_values.count(value)
        hand_copy = [card for card in hand_copy if
                     card.value != value]  # maybe not the best way to do this, as we create a new list every time
        if repetitions != 1:  # if we have a repetition
            max_repetitions = repetitions
            repetition_value = value
            second_run = get_num_repetitions(hand_copy)  # redo this function with the truncated list
            if second_run == 1:  # if we do not have a second repetition, just return the first find
                print('Duplicate Values is: ' + str([max_repetitions, repetition_value]))
                return [max_repetitions, repetition_value]
            else:  # if not, then return both the repetitions as a list (this means two pair, or a full house)
                repetitions_list = [[max_repetitions, repetition_value], second_run]
                print('Duplicate Values is: ' + sorted(repetitions_list, reverse=True))
                return sorted(repetitions_list, reverse=True)
    print('Duplicate Values is: ' + str([max_repetitions, repetition_value]))
    return [max_repetitions,
            repetition_value]  # if we get through every iteration, this should always return [1, rep_value]


def get_hand_types(hands):
    hand_types = []
    for hand in hands:
        hand_types.append(get_hand_type(hand))
    return hand_types


def determine_hand_winner(hands):
    #  input: list of list of Card Objects
    #  output: id of player who won
    # determine winner
    hand_types = get_hand_types(hands)
    print('Hand Type list: ' + str(hand_types))
    max_hand_type = max(hand_types)
    print('Max hand type is: ' + str(max_hand_type))
    indices = []
    for i, hand_type in enumerate(hand_types):  # Should be rewritten, loop is redundant, but deadlines
        if hand_type == max_hand_type:
            indices.append(i)
    print('Indices: ' + str(indices))
    if len(indices) > 1:
        if max_hand_type == 9:  # True tie
            return indices
        elif max_hand_type == 8:  # Higher straight flush wins, ties are possible
            max_value = 0
            max_index = -1
            for index in indices:
                hand = hands[index]
                if hand[0].value > max_value:
                    max_value = hand[0].value
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                elif hand[0].value == max_value:  # if a tie, do nothing
                    print('Tied Straight Flush')
                else:
                    indices.remove(index)  # otherwise, remove the loser
            return indices
        elif max_hand_type == 7:  # Higher 4 of a kind wins, can not tie
            max_value = 0
            max_index = -1
            for index in indices:
                hand = hands[index]
                if get_duplicate_values(hand)[0][1] > max_value:
                    max_value = get_duplicate_values(hand)[0][1]
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                else:
                    indices.remove(index)
        elif max_hand_type == 6:  # Ranked by triplet first and pair second
            max_hand = [0, 0]
            max_index = -1
            for index in indices:
                hand = hands[index]
                hand_value = get_duplicate_values(hand)
                if hand_value[0][1] > max_hand[0][1]:
                    max_hand = get_duplicate_values(hand)
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                elif hand_value[0][1] == max_hand[0][1]:  # if the 3 of a kind is a tie
                    if hand_value[1][1] > max_hand[1][1]:
                        max_hand = get_duplicate_values(hand)
                        if max_index != -1:
                            indices.remove(max_index)
                        max_index = index
                    else:
                        indices.remove(index)
                else:
                    indices.remove(index)
        elif max_hand_type == 5:  # Flush with the highest card wins
            max_value = 0
            max_index = -1
            for index in indices:
                hand = hands[index]
                hand_value = get_max_value(hand)
                if hand_value > max_value:  # Should be recursive, needs to be rewritten
                    max_value = hand_value
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                else:
                    indices.remove(index)
        elif max_hand_type == 4:  # Straight with the highest card wins
            max_value = 0
            max_index = -1
            for index in indices:
                hand = hands[index]
                hand_value = get_max_value(hand)
                if hand_value > max_value:
                    max_value = hand_value
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                else:
                    indices.remove(index)
        elif max_hand_type == 3:  # Highest 3 of a kind wins
            max_hand = [0, 0]
            max_index = -1
            for index in indices:
                hand = hands[index]
                hand_value = get_duplicate_values(hand)[0][1]
                if hand_value[0][1] > max_hand[0][1]:
                    max_hand = get_duplicate_values(hand)
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                else:
                    indices.remove(index)
        elif max_hand_type == 2:  # Highest Two Pair wins
            max_hand = [0, 0]
            max_index = -1
            for index in indices:
                hand = hands[index]
                hand_value = get_duplicate_values(hand)[0][1]
                if hand_value[0][1] > max_hand[0][1]:
                    max_hand = get_duplicate_values(hand)
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                elif hand_value[0][1] == max_hand[0][1]:  # If first pair is the same, check the second
                    if hand_value[1][1] > max_hand[1][1]:
                        max_hand = get_duplicate_values(hand)
                        if max_index != -1:
                            indices.remove(max_index)
                        max_index = index
                    else:
                        indices.remove(index)
                else:
                    indices.remove(index)
        elif max_hand_type == 1:  # Highest Pair wins
            max_hand = [0, 0]
            max_index = -1
            for index in indices:
                hand = hands[index]
                hand_value = get_duplicate_values(hand)
                print('Hand Value: ' + str(hand_value))
                if hand_value[1] > max_hand[1]:
                    max_hand = get_duplicate_values(hand)
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                elif hand_value[1] == max_hand[1]:  # If the pair is the same, check the kicker
                    if get_max_value(hands[index]) > get_max_value(hands[max_index]):
                        if max_index != -1:
                            indices.remove(max_index)
                        max_index = index
                    else:
                        indices.remove(index)
                else:
                    indices.remove(index)
        elif max_hand_type == 0:  # Highest card wins
            max_value = 0
            max_index = -1
            for index in indices:
                hand = hands[index]
                value = get_max_value(hand)
                if value > max_value:
                    max_value = value
                    if max_index != -1:
                        indices.remove(max_index)
                    max_index = index
                elif value == max_value:
                    if hand[1] > hands[max_index]:  # Should be recrusive, will need to be rewritten
                        if max_index != -1:
                            indices.remove(max_index)
                        max_index = index
                    else:
                        indices.remove(index)
                else:
                    indices.remove(index)
    print('Hand winner: ' + str(indices))
    return indices
