# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 23:20:42 2024

@author: jsham
"""


# --------- for use later maybe ---------------------------
#     player's next games
#from nba_api.stats.endpoints import playernextngames
#player_fture = playernextngames.PlayerNextNGames(player_id = player['id']).get_data_frames()[0]

# ------------------------

import pandas as pd

from nba_api.stats.static import players
from scipy.stats import poisson

# Your specific value and the average rate λ
value = 5  # For example, the number of events you're interested in
average = 10  # The λ (lambda) parameter of the Poisson distribution

# Calculate the probability of observing 'value' events
probability = poisson.pmf(value, average)

print("Probability:", probability)


# Step 1: Initialize the main list
leg_list = []
bet_prob_list = []

# Step 2: Enter a while loop
while True:
    # Ask the user for input; here we're expecting a comma-separated string
    leg_info = input("Enter Player Name, Leg Type, Leg Value, Home or Away,separated by commas, or 'done' to finish: ")
    
    # Break the loop if the user types 'done'
    if leg_info.lower() == 'done':
        break
    
    # Otherwise, split the string by commas into a list, and append this list to the main list
    sub_list = leg_info.split(',')
    leg_list.append(sub_list)

# Display the list of lists
print("Your bet list:")
print(leg_list)

#list of all players
player_dict = players.get_players()

for leg_ite in leg_list:

    player_name = leg_ite[0]
    
    player = [player for player in player_dict if player['full_name'].lower() == player_name.lower()][0]
    player_id = player['id']
    
    
    from nba_api.stats.endpoints import playergamelog
    #from nba_api.stats.library.parameters import SeasonAll
    
    gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = '2023')
    gamelog_player_df = gamelog_player.get_data_frames()[0]
    
    if leg_ite[3].lower() == "home":
        player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('vs', case=False, na=False)][['GAME_DATE', 'MATCHUP', 'PTS']]
        player_stats_average = player_stats[leg_ite[1]].mean()
        
    if leg_ite[3].lower() == "away":
        player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('@', case=False, na=False)][['GAME_DATE', 'MATCHUP', 'PTS']]
        player_stats_average = player_stats[leg_ite[1]].mean()
    
    print(player_stats)
    print(player_stats_average)
    
    probability = 1 - poisson.cdf(int(leg_ite[2])-1, player_stats_average)
    print("Probability:", probability)
    
    bet_prob_list.append(probability)


