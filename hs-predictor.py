import os
import pandas as pd
import numpy as np


def build_card_dict(card_dataframe):
    '''
    Helper function for get_card_probabilities, creates dict for counting decks 
    with/without a given card
    '''

    d = {}
    for card_name in card_dataframe['Name']:
        d[card_name] = 0
    return d


def enter_card(remaining_decks):
    '''
    Prompt user for card played, subsets possible decks containing that card
    '''

    while True:
        try:
            card_played = input('Card played: ')
            return card_played, remaining_decks.loc[remaining_decks[card_played] == 1]
        except KeyError:
            print('Card not found in any decks.')


def get_card_probabilities(decks, all_cards):
    '''
    Puts cards into dict where dict[name] is the probability a given card 
    appears in a deck
    '''

    # Create dict of all Hearthstone cards
    card_dict = build_card_dict(all_cards)
    if len(decks) == 0:
        return card_dict

    # for each possible card, calculate probability as sum of games played by 
    # decks with that card divided by total games played by all decks
    total_games = decks['Games Played'].sum()
    for idx, row in decks.iterrows():
        for card_name in all_cards['Name']:
            if row[card_name] == 1:
                card_dict[card_name] += row['Games Played'] / total_games

    return card_dict


def get_class_data_from_csv():
    '''
    Reads csv file for a specific Hearthstone class
    '''

    while True:
        try:
            opponent_class = input("Enter opponent's class: ").lower()
            return pd.read_csv(os.path.join('class-data', '{}-decks.csv'.format(opponent_class)))
        except FileNotFoundError:
            print('Class file not found. Try again.')


def print_game_state(sorted_cards, cards_seen):
    '''
    Display cards and their probabilities, and cards already seen, to the user
    '''

    print()
    print("Cards likely in opponent's deck:")
    for card_name, prob in sorted_cards:
        if (prob > 0.05) and (card_name not in cards_seen):
            print('   {}| {} %'.format(card_name.ljust(25), str(round(prob*100, 1))))

    print('Cards already played:')
    for card in cards_seen:
        print('   {}'.format(card))
    print()


def main():
    '''
    While the game is being played, continually ask the user for cards played
    by the opponent and show the probabilities that other cards are included
    '''
    
    # Import all card data
    all_card_data = pd.read_csv('allcarddata.csv')

    # Read top deck data for opponent's class
    possible_decks = get_class_data_from_csv()

    # Begin playing the game
    cards_seen = []
    while True:
        # Get user input about card played by opponent, subset decks accordingly
        card_played, possible_decks = enter_card(possible_decks)
        cards_seen.append(card_played)

        # Get sorted list of cards from most to least likely
        sorted_cards = sorted(get_card_probabilities(possible_decks, all_card_data).items(), 
            key=lambda x: x[1], reverse=True)

        print_game_state(sorted_cards, cards_seen)

        # Ask to continue or quit
        done_playing = input('Press enter to continue, or type "done" to stop. \n')
        if done_playing.lower() == 'done':
            break

if __name__ == '__main__':
    main()