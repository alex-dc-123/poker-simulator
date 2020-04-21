# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:01:33 2020

@author: adr01
"""

from iteration_utilities import duplicates

# create a dictionary for each hand, first variable representing card number and second representing suit
def create_deck_fn():
    deck = {}
    suits = ['H', 'D', 'C', 'S']
    
    # create the deck
    for suit in suits:
        for card in range(1,14):
            deck[(str(card) + suit)] = [card,suit]
    return deck
       
# Move cards from the deck to the hand
def table_fn(cards, turn_cards):
    for card in cards:
        turn_cards[card] = deck[card]
        deck.pop(card, None)
    return turn_cards

# count appearance of each number and each suit. if part = 0 then pairs, if 1 then suits
def split_check_fn(part):
    check = {}
    for card_number in turn_cards.values():
       value = card_number[part]
       if value in check.keys():
           check[value] += 1
       else: 
           check[value] = 1
    return check

# Split the hands into their pairings
def check_matches_fn(matches):
    pk_hand = []
    for i in range(len(pair_check)):
        if list(pair_check.values())[i] == matches:
            pk_hand.append(list(pair_check.keys())[i])
    pk_hand.sort(reverse=True)
    return pk_hand# .sort(reverse = True)


# set out hand 
my_hand = ['2H', '4C']
flop = ['3H', '5C', '9S']
turn = ['13H'] 
river = ['5S']

# user inputs their hand
deck = create_deck_fn()

# change deck and turn cards
turn_cards = table_fn(my_hand, {})
turn_cards = table_fn(flop, turn_cards)
turn_cards = table_fn(turn, turn_cards)
turn_cards = table_fn(river, turn_cards)

pair_check = split_check_fn(0)
flush_check = split_check_fn(1)
     
pk_quads = check_matches_fn(4)
pk_set = check_matches_fn(3)
pk_pair = check_matches_fn(2)
pk_high = check_matches_fn(1)



if len(check_matches_fn([],4)) > 0:
    pk_quads = check_matches_fn([],4)
if len(check_matches_fn([],3)) > 0:
    pk_set = check_matches_fn([],3)
if len(check_matches_fn([],2)) > 0:
    pk_pair = check_matches_fn([],2)
if len(check_matches_fn([],1)) > 0:
    pk_high = check_matches_fn([],1)
    
    
