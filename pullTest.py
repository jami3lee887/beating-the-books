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
from nba_api.stats.endpoints import playergamelog
import numpy as np

# Your data organized into a dictionary
starters_data = {
    'Team': ["Atlanta Hawks"] * 5 + ["Boston Celtics"] * 5 + ["Brooklyn Nets"] * 5 + ["Charlotte Hornets"] * 5 +
            ["Chicago Bulls"] * 5 + ["Cleveland Cavaliers"] * 5 + ["Dallas Mavericks"] * 5 + ["Denver Nuggets"] * 5 +
            ["Detroit Pistons"] * 5 + ["Golden State Warriors"] * 5 + ["Houston Rockets"] * 5 + ["Indiana Pacers"] * 5 +
            ["Los Angeles Clippers"] * 5 + ["Los Angeles Lakers"] * 5 + ["Memphis Grizzlies"] * 5 + ["Miami Heat"] * 5 +
            ["Milwaukee Bucks"] * 5 + ["Minnesota Timberwolves"] * 5 + ["New Orleans Pelicans"] * 5 +
            ["New York Knicks"] * 5 + ["Oklahoma City Thunder"] * 5 + ["Orlando Magic"] * 5 + ["Philadelphia 76ers"] * 5 +
            ["Phoenix Suns"] * 5 + ["Portland Trail Blazers"] * 5 + ["Sacramento Kings"] * 5 + ["San Antonio Spurs"] * 5 +
            ["Toronto Raptors"] * 5 + ["Utah Jazz"] * 5 + ["Washington Wizards"] * 5,
    'Player': [
        "Trae Young", "Dejounte Murray", "De'Andre Hunter", "Saddiq Bey", "Clint Capela",
        "Jrue Holiday", "Derrick White", "Jaylen Brown", "Jayson Tatum", "Kristaps Porzingis",
        "Spencer Dinwiddie", "Cam Thomas", "Mikal Bridges", "Cameron Johnson", "Nicolas Claxton",
        "LaMelo Ball", "Terry Rozier", "Brandon Miller", "P.J. Washington", "Mark Williams",
        "Coby White", "Alex Caruso", "Zach LaVine", "DeMar DeRozan", "Nikola Vucevic",
        "Darius Garland", "Donovan Mitchell", "Max Strus", "Evan Mobley", "Jarrett Allen",
        "Luka Doncic", "Kyrie Irving", "Josh Green", "Grant Williams", "Dereck Lively II",
        "Jamal Murray", "Kentavious Caldwell-Pope", "Michael Porter Jr.", "Aaron Gordon", "Nikola Jokic",
        "Cade Cunningham", "Jaden Ivey", "Ausar Thompson", "Isaiah Stewart", "Jalen Duren",
        "Stephen Curry", "Klay Thompson", "Andrew Wiggins", "Draymond Green", "Kevon Looney",
        "Fred VanVleet", "Jalen Green", "Dillon Brooks", "Jabari Smith Jr.", "Alperen Sengün",
        "Tyrese Haliburton", "Bennedict Mathurin", "Bruce Brown", "Obi Toppin", "Myles Turner",
        "Russell Westbrook", "James Harden", "Paul George", "Kawhi Leonard", "Ivica Zubac",
        "D'Angelo Russell", "Austin Reaves", "Taurean Prince", "LeBron James", "Anthony Davis",
        "Marcus Smart", "Desmond Bane", "Ziaire Williams", "Jaren Jackson Jr.", "Xavier Tillman Sr.",
        "Kyle Lowry", "Tyler Herro", "Jimmy Butler", "Caleb Martin", "Bam Adebayo",
        "Damian Lillard", "Malik Beasley", "Khris Middleton", "Giannis Antetokounmpo", "Brook Lopez",
        "Mike Conley", "Anthony Edwards", "Kyle Anderson", "Karl-Anthony Towns", "Rudy Gobert",
        "CJ McCollum", "Herbert Jones", "Brandon Ingram", "Zion Williamson", "Jonas Valanciunas",
        "Jalen Brunson", "Quentin Grimes", "RJ Barrett", "Julius Randle", "Mitchell Robinson",
        "Shai Gilgeous-Alexander", "Josh Giddey", "Jalen Williams", "Kenrich Williams", "Chet Holmgren",
        "Cole Anthony", "Jalen Suggs", "Franz Wagner", "Paolo Banchero", "Wendell Carter Jr.",
        "Tyrese Maxey", "De'Anthony Melton", "Tobias Harris", "Robert Covington", "Joel Embiid",
        "Bradley Beal", "Devin Booker", "Josh Okogie", "Kevin Durant", "Jusuf Nurkic",
        "Scoot Henderson", "Anfernee Simons", "Matisse Thybulle", "Jerami Grant", "Deandre Ayton",
        "De'Aaron Fox", "Kevin Huerter", "Harrison Barnes", "Keegan Murray", "Domantas Sabonis",
        "Jeremy Sochan", "Devin Vassell", "Keldon Johnson", "Victor Wembanyama", "Zach Collins",
        "Scottie Barnes", "Gary Trent Jr.", "OG Anunoby", "Pascal Siakam", "Jakob Poeltl",
        "Talen Horton-Tucker", "Jordan Clarkson", "Lauri Markkanen", "John Collins", "Walker Kessler",
        "Tyus Jones", "Jordan Poole", "Deni Avdija", "Kyle Kuzma", "Daniel Gafford"
    ]
}

# Create DataFrame
teams_n_players = pd.DataFrame(starters_data)
extended_df = pd.DataFrame(starters_data)


# ------- for finding info tags
#player_dict = players.get_players()
#player = [player for player in player_dict if player['full_name'].lower() == "trae young"][0]
#player_id = player['id']
#gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = '2023')
#gamelog_player_df = gamelog_player.get_data_frames()[0]

def boostedparlay():
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
        
        

        #from nba_api.stats.library.parameters import SeasonAll
        
        gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = '2023')
        gamelog_player_df = gamelog_player.get_data_frames()[0]
        
        if leg_ite[3].lower() == "home":
            player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('vs', case=False, na=False)][['GAME_DATE', 'MATCHUP', leg_ite[1]]]
            player_stats_average = player_stats[leg_ite[1]].mean()
            
        if leg_ite[3].lower() == "away":
            player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('@', case=False, na=False)][['GAME_DATE', 'MATCHUP', leg_ite[1]]]
            player_stats_average = player_stats[leg_ite[1]].mean()
        
        print(player_stats)
        print(player_stats_average)
        
        probability = 1 - poisson.cdf(int(leg_ite[2])-1, player_stats_average)
        print("Probability:", probability)
        
        print("decimal payout should be: ",round(1/probability,2))
        bet_prob_list.append(probability)


def quickTeamOdds(team,homeOrAway):
    team_df = teams_n_players[teams_n_players['Team'] == team]
    
    odds_list = []
    probs_list = []
    bet_kinds = ["10+ PTS", "15+ PTS", "20+ PTS", "25+ PTS", "30+ PTS", "1+ 3's", "2+ 3's", "3+ 3's", "4+ 3's", "5+ 3's", 
                 "4+ Rebs", "6+ Rebs", "8+ Rebs", "10+ Rebs", "12+ Rebs", "14+ Rebs", "16+ Rebs",
                 "2+ ASTs", "4+ ASTs", "6+ ASTs", "8+ ASTs", "10+ ASTs", "12+ ASTs",]
    
    
    #list of all players
    player_dict = players.get_players()
    
    for i in team_df['Player']:
        
        player = [player for player in player_dict if player['full_name'].lower() == i.lower()][0]
        player_id = player['id']
        
        
        gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = '2023')
        gamelog_player_df = gamelog_player.get_data_frames()[0]
        
        if homeOrAway.lower() == "home":
            player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('vs', case=False, na=False)]
        
        if homeOrAway.lower() == "away":
            player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('@', case=False, na=False)]
            
            
        player_avg_pts = round(player_stats["PTS"].mean(),2)
        player_avg_FG3M = round(player_stats["FG3M"].mean(),2)
        player_avg_REB = round(player_stats["REB"].mean(),2)
        player_avg_AST = round(player_stats["AST"].mean(),2)
        
        #print(player_avg_pts)
        #print(player_avg_FG3M)
        #print(player_avg_REB)
        #print(player_avg_AST)
        
        for i in [10, 15, 20, 25, 30]:
            prob = 1 - poisson.cdf(i-1, player_avg_pts)
            #print(prob)
            if prob < 0.01:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
        for i in [1,2,3,4,5]:
            prob = 1 - poisson.cdf(i-1, player_avg_FG3M)
            if prob < 0.01:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
        for i in [4,6,8,10,12,14,16]:
            prob = 1 - poisson.cdf(i-1, player_avg_REB)
            if prob < 0.01:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
        for i in [2,4,6,8,10,12]:
            prob = 1 - poisson.cdf(i-1, player_avg_AST)
            if prob < 0.01:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
            
            
    print(odds_list)
    print(len(odds_list))
    
    print(probs_list)
    print(len(probs_list))
        
    # Reshape the odds_list into a 5x24 DataFrame
    odds_df = pd.DataFrame(np.reshape(odds_list, (5, 23)), columns=bet_kinds)
    extended_df = pd.concat([team_df.reset_index(drop=True), odds_df], axis=1)
    print(extended_df)
    extended_df.to_csv("bet_stamps.csv",index=False)
        
        
    
    
