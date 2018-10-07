#!/usr/bin/env python3

import pandas as pd
import numpy as np

# Helper function for get_card_probabilities, creates dict for counting decks with/without a given card
def build_card_dict(card_dataframe):
    d = {}
    for card_name in card_dataframe["Name"]:
        d[card_name] = 0
    return d

# Builds a dataframe from the raw deck csv
def build_deck_dataframe(index, deck_csv, all_cards):
    new_deck = pd.DataFrame(data=np.zeros((1, all_cards.shape[0]), dtype=int), columns=all_cards["Name"])
    for idx2, card in deck_csv.iteritems():
        if type(card) == str:
            # Clean card names based on scraping results
            card = card.replace(",", "")
            # Account for the column that shows Games Played, which is not a card
            if card.isdigit():
                new_deck["Games Played"] = int(card)
            else:
                for char in "★×2":
                    card = card.replace(char, "")
                if card[len(card) - 1] == " ":
                    card = card[:len(card) - 1]
                new_deck[card] = 1
    new_deck["Deck Name"] = index
    return new_deck

# General function for converting dict to list of tuples, for easy sorting
def convert_dict_to_list(my_dict):
    dict_list = []
    for key, value in my_dict.items():
        if value != 0:
            dict_list.append((value, key))
    dict_list.sort(reverse=True)
    return dict_list

# Puts cards into dict where dict[name] is the probability a given card appears in a deck
def get_card_probabilities(all_possible_decks, all_cards):
    if len(all_possible_decks) == 0:
        return []
    card_dict = build_card_dict(all_cards)
    for card_name in all_possible_decks.columns.values:
        included = 0
        for val in all_possible_decks[card_name]:
            if val == 1:
                included += 1
        card_dict[card_name] = included / len(all_possible_decks[card_name])
    return convert_dict_to_list(card_dict)

# Reads csv file for a specific Hearthstone class
def get_class_data_from_csv():
    while True:
        try:
            opponent_class = input("Enter opponent's class: ").lower()
            return pd.read_csv(opponent_class + "data.csv", index_col="Deck Name")
        except FileNotFoundError:
            print("Class not found. Try again.")

# Prompt user for card played, subsets possible decks containing that card
def get_possible_decks(remaining_decks):
    while True:
        try:
            card_played = input("Card played: ")
            return remaining_decks.loc[remaining_decks[card_played] == 1]
        except KeyError:
            print("Card not found in any decks.")

def main():
	# Import all card data
    all_card_data = pd.read_csv('allcarddata.csv')

    # Read top deck data for opponent's class
    class_data = get_class_data_from_csv()

    # Build dataframe for class used by opponent
    # Data frame 'decks' contains all cards in Hearthstone as columns, where each row is a different deck.
    # Cell value is 1 if deck (represented by row) contains card (represented by column), 0 otherwise
    decks = pd.DataFrame(columns=all_card_data["Name"])
    for idx, deck_row in class_data.iterrows():
        decks = decks.append(build_deck_dataframe(idx, deck_row, all_card_data), sort=False)
    decks.index = range(len(decks.index))

    # Enter cards until user says game is over
    possible_decks = decks
    while True:
        possible_decks = get_possible_decks(possible_decks)
        print()
        for prob, card_name in get_card_probabilities(possible_decks, all_card_data):
        	if prob > 0.2:
        		print("   " + card_name.ljust(25) + "| " + str(round(prob*100, 1)) + " %")
        print()

        done_playing = input("Done? [y/n] \n")
        if done_playing == 'y':
            break

if __name__ == "__main__":
	main()