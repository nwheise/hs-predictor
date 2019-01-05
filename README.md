# hs-predictor
A simple project for predicting an opponent's deck in Hearthstone.  
Python Version 3.6.6

The script allows the user to enter the opponent's class and then, as the game is being played, enter what cards are used by the opponent.  
After each card is entered, the script returns the list of possible cards in the opponent's deck with the corresponding probability that the card is included.  
Probabilities are calculated by counting the games played by decks including the cards already played, divided by the total number of games for which we have data.  


The scrape-decks.py script should be run first, to scrape the most popular recent decks being used.    
The scraper uses selenium to scrape deck data from hsreplay.net, and beautifulsoup to parse the html and obtain the relevant information.
Then, run hs-predictor.py while playing Hearthstone and enter the cards used by the opponent as they appear.  


# Credit
Hearthstone deck data was scraped from hsreplay.net -  
https://hsreplay.net/  

Data for all cards was obtained from the public Google doc here -  
https://docs.google.com/spreadsheets/d/1tYuukT1O3qdvbSfpUAbJMJLYkusXclc-Rivd-uMy6g0/edit#gid=661942186  

# Contact Information  
Name: Nick Heise  
Email: me@nh.cool   
