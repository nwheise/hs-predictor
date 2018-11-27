import os
import sys
import pandas as pd
import numpy as np
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from bs4 import BeautifulSoup


def scrape_pages(class_name):
    '''
    Uses FireFox webdriver to scrape webpages for the class given.
    input class_name should be type string in all caps (HUNTER, DRUID, etc.)
    '''

    # Set up the FireFox webdriver
    os.environ['MOZ_HEADLESS'] = '1'
    binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe', log_file=sys.stdout)
    driver = webdriver.Firefox(firefox_binary=binary)

    # Get the html soups with BeautifulSoup
    soup_list = []
    for i in range(30):
        driver.get('https://hsreplay.net/decks/#playerClasses={}&page={}'.format(class_name, i))
        soup_list.append(BeautifulSoup(driver.page_source, 'html.parser'))
    driver.quit()

    return soup_list


def create_deck_row(tile_soup, all_card_data):
    '''
    Creates a pandas dataframe whose columns are all cards in Hearthstone, 
    where the row val is 1 if the card is including in the deck and 0 otherwise.
    '''

    # Separate deck name, games played, and the cards
    deck_name = tile_soup.find('span', attrs={'class': 'deck-name'}).string 
    game_count = tile_soup.find('span', attrs={'class': 'game-count'}).string
    card_list = tile_soup.find('ul', attrs={'class': 'card-list'})
    
    # Create a list of the card names
    cards = []
    for card in card_list.find_all('a'):
        cards.append(card.find('div')['aria-label'])

    # Initialize the dataframe
    new_deck = pd.DataFrame(data=np.zeros((1, all_card_data.shape[0])))
    new_deck.columns = all_card_data['Name']

    # Clean card names and change dataframe value to 1 to show it's included
    for card_str in cards:
        for char in '★×2':
            card_str = card_str.replace(char, '')
        if card_str[-1] == ' ':
            card_str = card_str[:-1]

        new_deck[card_str] = 1

    new_deck['Deck Name'] = deck_name
    new_deck['Games Played'] = int(game_count.replace(',', ''))
    
    return new_deck


def scrape_class(class_name, all_card_data):
    '''
    Takes the class name and scrapes the top deck data for that class from 
    HS Replay. Saves the deck data in a csv file.
    '''

    # Get the soups for the pages associated with the class
    soup_list = scrape_pages(class_name)

    # Set up the dataframe for all the class decks
    decks_df = pd.DataFrame()

    # Go through webpages and add each deck to the dataframe
    for page_soup in soup_list:
        deck_tiles = page_soup.find_all('div', attrs={'class': 'deck-tile'})
        for tile in deck_tiles:
            decks_df = decks_df.append(create_deck_row(tile, all_card_data), 
                ignore_index=True,
                sort=False)

    # Write to the csv file
    if not os.path.isdir('class-data'): 
        os.makedirs('class-data')
    decks_df.to_csv(os.path.join('class-data', 
        '{}-decks.csv'.format(class_name.lower())))


def main():
    '''
    Scrape the data for all classes and save them in csv files
    '''

    all_card_data = pd.read_csv('allcarddata.csv')
    hs_classes = ['DRUID', 'HUNTER', 'MAGE', 'PALADIN', 'PRIEST', 'ROGUE', 
        'SHAMAN', 'WARLOCK', 'WARRIOR']
    for c in hs_classes:
        scrape_class(c, all_card_data)
        print('{} decks successfully scraped.'.format(c))


if __name__ == '__main__':
    main()