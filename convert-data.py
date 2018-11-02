#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os

# Reformat the deck dataframe from the scraped data to the standard format used by hs-predictor
def build_deck_dataframe(deck_row, all_cards):
    new_deck = pd.DataFrame(data=np.zeros((1, all_cards.shape[0]), dtype=int))
    new_deck.columns = all_cards['Name']

    cards = deck_row.drop(labels=['Deck Name', 'Games Played'])
    cards.dropna(inplace=True)
    for i, card in cards.iteritems():
        # Clean card names based on scraping results
        for char in "★×2":
            card = card.replace(char, "")
        if card[-1] == " ":
            card = card[:-1]
        new_deck[card] = 1

    new_deck["Deck Name"] = deck_row['Deck Name']
    new_deck['Games Played'] = int(deck_row['Games Played'].replace(',', ''))

    return new_deck

def main():
    # Read data for all cards in Hearthstone
    all_card_data = pd.read_csv('allcarddata.csv')

    hs_classes = ['druid', 'hunter', 'mage', 'paladin', 'priest', 'rogue', 'shaman', 'warlock', 'warrior']
    for c in hs_classes:
        # Read the scraped data for the class
        raw_df = pd.read_csv("./scraped-class-data/" + c + "data.csv")

        # Create converted_df where the columns are all existing cards in Hearthstone
        converted_df = pd.DataFrame(columns=all_card_data['Name'])

        # Convert each deck in the scraped data into the standard format and add to the converted_df
        for idx, deck_row in raw_df.iterrows():
            converted_df = converted_df.append(build_deck_dataframe(deck_row, all_card_data), sort=False)
        converted_df.index = range(len(converted_df.index)) 

        # Save standardized class data to be used by hs-predictor
        if not os.path.isdir('converted-class-data'): os.makedirs('converted-class-data')
        converted_df.to_csv('converted-class-data/' + c + '-converted.csv', index='Deck Name')
        print(c + ' data has been converted')

if __name__ == "__main__":
    main()