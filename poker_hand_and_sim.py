import random
from itertools import chain
import numpy as np
#### Section 1 
#### Create the deck and creating player and opponent hands

# create a dictionary for each hand, first variable representing card number and second representing suit
def create_deck_fn():
    deck = {}
    suits = ['H', 'D', 'C', 'S']
    
    # create the deck
    for suit in suits:
        for card in range(2,15):
            deck[(str(card) + suit)] = [card,suit]
    return deck
       
# User Inputs their own cards and the flop cards
# Removes the cards from the deck and stores in seperate dictionary
# Cards represents the string of card names and turn_cards represents the dicitonary
def table_fn(cards, turn_cards, deck):
    for card in cards:
        turn_cards[card] = deck[card]
        deck.pop(card, None)
    return turn_cards

# Create a dictionary combining the cards (either yours or opponents) to the cards on the table.
# Same as function before, but adding from the table to the hand rather than the deck to the table and not removing
def hand_fn(cards, turn_cards):
    for card in turn_cards:
        cards[card] = turn_cards[card]
    return cards

# Takes the number of opponents as an input
# For each opponent generate 2 cards from the random_cards_fn, and the cards on the flop to the dictionary
# store in a dictionary of dictionaries with the key for each opponent going Opp_0, Opp_1 ...
def opponent_hands_fn(opponents, deck, turn_cards):
    opp_hands = {}
    for player in range(opponents):
        opp_cards = random_cards_fn(deck, 2)
        player_cards = hand_fn(opp_cards, turn_cards)
        player_name = 'Opp_' +  str(player)
        opp_hands[player_name] = player_cards       
    return opp_hands

# Pull 2 random cards from the deck into a dictionary and return
def random_cards_fn(deck, cards):
    opp_hand = {}
    for i in range(cards):
        opp_card = random.choice(list(deck.keys()))
        opp_hand[opp_card] = deck[opp_card]
        deck.pop(opp_card, None)
    return opp_hand


#### Section 2 
#### Evaluating the strength of any players hands. 

# Counts occurances of each number or each suit 
# if part = 0 then number, if 1 then suit
def split_check_fn(part, player_cards):
    check = {}
    for card_number in player_cards.values():
       value = card_number[part]
       if value in check.keys():
           check[value] += 1
       else: 
           check[value] = 1
    return check

# Use matches to determine number of occurances of a number/suit i.e. matches = 4 would find quads, matches = 3 would find number of sets
# if that hand appears (i.e. pair, set) then add that value to a list and return in descending order  
# Get value of all cards for high cards for comparing hands of same strength later
def check_matches_fn(matches, pair_check):
    pk_hand = []
    if matches == 1:
        pk_hand = list(pair_check.keys())
    else:
        for i in range(len(pair_check)):
            if list(pair_check.values())[i] == matches:
                pk_hand.append(list(pair_check.keys())[i])
    pk_hand.sort(reverse=True)
    return pk_hand

# first check if flush, if it isnt return empty,
# Filter for all card numbers that are the suit of the flush and then check for a straight
def straight_flush_fn(flush_check, player_cards):
    
    # if no flush return nothing
    if len(flush_check_fn(flush_check, player_cards)) == 0:
        return []
    flush_suit = flush_check_fn(flush_check, player_cards)[1]
    # Create list of numbers that are of the same suit as the flush
    flush_list = []
    for cards in player_cards.values():
        if cards[1] == flush_suit:
            flush_list.append(cards[0])
    if 14 in flush_list:
        flush_list.append(1)        
    flush_list.sort()
    # Check if straight
    straight_start = 0
    for i in range(0,3):
        if flush_list[i:i+5] == list(range(flush_list[i],flush_list[i]+5)):
            straight_start = max(straight_start, flush_list[i]) 
    if straight_start > 0:
        return [list(range(straight_start, straight_start + 5)), flush_suit]
    else:
        return []
    
# For each suit check the number of appearances
# If greater than 5, put all the cards of that suit into a list and return the top 5
def flush_check_fn(flush_check, player_cards):
    for i in range(len(flush_check)):
        if list(flush_check.values())[i] >= 5:
            suit =  list(flush_check.keys())[i]
            flush_order = [] 
            for card in player_cards.values():
                if card[1] == suit:
                    flush_order.append(card[0])
                    
            flush_order.sort(reverse = True)
            return [flush_order[:5], suit]
    return []

# go through all the values and determine if 5 consecutive numbers
def staight_check_fn(pair_check):
    card_order = list(pair_check.keys())
    # if less than 5 cards cant be a straight so return nothin
    if len(card_order) < 5:
        return []
    # Let ace be seen as both 14 as 1 for straights on either sides
    if 14 in card_order:
        card_order.append(1)
    card_order.sort()  
    # Want to find the maximum straight
    straight_start = 0
    for i in range(0,len(card_order) - 4):
        if card_order[i:i+5] == list(range(card_order[i],card_order[i]+5)):
            straight_start = max(straight_start, card_order[i])
    
    if straight_start > 0:
        return list(range(straight_start,straight_start+5))    
    else:
        return []

# In order of rank go through each hand to check if you have it and return the highest hand you do have
# If hand doesn't have 5 cards include the high cards
def hand_assessment_fn(pair_check, flush_check, pk_quads, pk_set, pk_pair, pk_high, player_cards):
    # go through all hand posibilties in order of rank 
    # return the hand and the 5 top cards
    if len(straight_flush_fn(flush_check, player_cards)) > 0:
        return [8, 'Straight Flush', straight_flush_fn(flush_check, player_cards)[0], straight_flush_fn(flush_check, player_cards)[1]]
    elif len(pk_quads) > 0:
        return [7, 'Quads', pk_quads[0], high_card_fn(pk_high, [pk_quads[0]], 1)]
    elif (len(pk_set) > 1):
        return [6, 'Full House', [pk_set[0], pk_set[1]], []]
    elif (len(pk_set) == 1) & (len(pk_pair) >= 1):
        return [6, 'Full House', [pk_set[0], pk_pair[0]], []]
    elif len(flush_check_fn(flush_check, player_cards)) > 0:
        return [5, 'Flush', flush_check_fn(flush_check, player_cards)[0], flush_check_fn(flush_check, player_cards)[1]]
    elif len(staight_check_fn(pair_check)) > 0:
        return [4, 'Straight', staight_check_fn(pair_check), []]
    elif len(pk_set) > 0:
        return [3, 'Set', pk_set[0], high_card_fn(pk_high, [pk_set[0]], 2)]
    elif len(pk_pair) > 1:
        return [2, '2 Pair', pk_pair[:2], high_card_fn(pk_high, pk_pair[:2], 1)]
    elif len(pk_pair) == 1:
        return [1, 'Pair', pk_pair[0], high_card_fn(pk_high, [pk_pair[0]], 3)]
    else:
        return [0, 'high cards', [], pk_high[:5]]

# Define the remaining high cards for each hand
def high_card_fn(pk_high, hand, remaining):
    for number in hand:
        pk_high.remove(number)
    pk_high.sort(reverse = True)
    return pk_high[:remaining]

# Output the highest ranked hand the player has
def poker_hand_fn(player_cards):
    # find the occurences of all numbers and suits
    pair_check = split_check_fn(0, player_cards)
    flush_check = split_check_fn(1, player_cards)
         
    # find all number variations
    pk_quads = check_matches_fn(4, pair_check)
    pk_set = check_matches_fn(3, pair_check)
    pk_pair = check_matches_fn(2, pair_check)
    pk_high = check_matches_fn(1, pair_check)
    # return hand
    return hand_assessment_fn(pair_check, flush_check, pk_quads, pk_set, pk_pair, pk_high, player_cards)

#### Section 3
#### Comparing your hand to your opponents

# Look at the rank of your hand and compare it to all your opponents
# if they have higher you lose, if you have the same you have to do further checks
# store opponents hands if they are the same resk in order to check winners
def winning_hand(player_cards, opponent_cards):
    hand_rank = poker_hand_fn(player_cards)[0]
    opponent_rank = 0
    opponent_list = []
    # loop through each opponent to see if their hand is better than the players
    # use the keys (list of opponents) to pull the dictionary of their cards
    for opponent in opponent_cards.keys():
        opponent_hand = opponent_cards[opponent]
        temp_opponent_rank = poker_hand_fn(opponent_hand)[0]
        # if opponent is better break immediately
        if temp_opponent_rank > hand_rank:
            return False, False
        # if the same store player name for comparison later
        elif temp_opponent_rank == hand_rank:
            opponent_order = poker_hand_fn(opponent_hand)
            opponent_list.append(opponent_order)
        # store maximum rank of opponent
        opponent_rank = max(temp_opponent_rank, opponent_rank)

    if opponent_rank < hand_rank:
        return True, True
    else:
        return same_hand_compairson_fn(hand_rank, opponent_list, poker_hand_fn(player_cards))

# Depending on the rank of the hand will either need to check the cards or the high cards to see who wins
# straight flush, flush and straight can all be decided by who has the highest value
# Quads, set, 2 pair, pair or high card all determined by who has the highest card outside
# full house done on set then pair
def same_hand_compairson_fn(hand_rank, opponent_list, player_result):
    if hand_rank in [4,5,8]: 
        player_hand = player_result[2]
        return compare_hand_fn(opponent_list, player_hand, 2)
    elif hand_rank in [0,1,2,3,7]:
        player_hand = player_result[3]
        return compare_hand_fn(opponent_list, player_hand, 3)
    elif hand_rank == 6:
        player_hand = player_result[2]
        return compare_fh_fn(opponent_list, player_hand)

# The key represents to look at the opponents hand or high cards
# It combines all the opponent hands into one list and finds the cards that 
def compare_hand_fn(opponent_list, player_hand, key):
    all_oponent_cards = []
    for opponent_cards in opponent_list:
        all_oponent_cards.append(opponent_cards[key])
    all_oponent_cards = list(chain.from_iterable(all_oponent_cards))
    player = np.setdiff1d(player_hand,all_oponent_cards)
    opponent = np.setdiff1d(all_oponent_cards,player_hand)
    # if all cards in each others hand will be array of size 0 so cant use max function so this gets around that 
    if len(player) == 0: 
        player = [0,0]
    if len(opponent) == 0:
        opponent = [0,0]
    # Find the max card not in eachothers hands to see whose is better
    player_max = max(player)
    opponent_max = max(opponent)
    
    return compare_judge_fn(player_max, opponent_max)
    
# Compare the set of your hand and your opponents
# if set is the same compare the pairs    
def compare_fh_fn(opponent_list, player_hand):
    
    player_set = player_hand[0] 
    opp_set = 0
    opponent_pair_list = []
    for opponent_sets in opponent_list:
        temp_set = opponent_sets[2][0]
        if temp_set > player_set:
            return False, False 
        elif temp_set == player_set:
            opponent_pair_list.append(opponent_sets[2][1])
        opp_set = max(temp_set, opp_set)
    # Analyse who has the better set 
    if player_set > opp_set:
        return True, True
    elif player_set == opp_set:
        player_pair = player_hand[1]
        opp_pair = 0
        for opponent_pair in opponent_pair_list:
            opp_pair = max(opp_pair, opponent_pair)
        return compare_judge_fn(player_pair, opp_pair)
    else:
        return False, False        

# Return function for the two functions above
def compare_judge_fn(player, opp):        
    if player > opp:
        return True, True
    elif player == opp:
        return True, False
    else: 
        return False, False
    
#### Section 4
#### Monte Carlo Simulation to see how many tumes you win that hand
# Fist step is to simulate hands once all cardss are drawn,
# next add feature so can randomise turn and flop and then opponent cards.

def pot_win(my_hand, flop, turn, river, opponents):
    deck = create_deck_fn()
    player_cards = table_fn(my_hand, {}, deck)

    flop, turn, river = table_card_fn(flop, turn, river, deck)
    turn_cards = hand_fn(flop, turn)    
    turn_cards = hand_fn(turn_cards, river)
    
    player_cards = hand_fn(player_cards, turn_cards)      
    opponent_cards = opponent_hands_fn(opponents, deck, turn_cards) #  
    # print(opponent_cards)
    return winning_hand(player_cards, opponent_cards)

def simulation_fn(my_hand, flop, turn, river, opponents, iterations):
    win, loss, split = 0,0,0
    for i in range(iterations):
        pot_1, pot_2 = pot_win(my_hand, flop, turn, river, opponents)
        if (pot_1 == False) and (pot_2 == False):
            loss += 1
        elif (pot_1 == True) and (pot_2 == False):
            split += 1
        elif (pot_1 == True) and (pot_2 == True):
            win += 1
    
    return round(loss * 100 / iterations, 2), round(split * 100 / iterations, 2), round(win * 100 / iterations, 2)

def table_card_fn(flop, turn, river, deck):
    if len(flop) == 0:
        flop = random_cards_fn(deck, 3)
    else:
        flop = table_fn(flop, {}, deck)
    if len(turn) == 0:
        turn = random_cards_fn(deck, 1)
    else:
        turn = table_fn(turn, {}, deck)
    if len(river) == 0:
        river = random_cards_fn(deck, 1)
    else:
        river = table_fn(river, {}, deck)
    return flop, turn, river
    


#### Section 4
#### Analyse Hand 
my_hand = ['12D', '14S']
flop = ['4H', '6H', '10D']
turn = [] 
river = []
    
    
# set out hand
#my_hand = ['14H', '13D']

#turn = ['7C'] 
#river = ['7S']

opponents = 2
iterations = 10000
simulation_fn(my_hand, flop, turn, river, opponents, iterations)
#start = time.time()
#print(simulation_fn(my_hand, flop, turn, river, opponents, iterations))
#end = time.time()
#print(end - start)







