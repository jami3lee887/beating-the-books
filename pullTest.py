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
import datetime
from nba_api.stats.static import players
from scipy.stats import poisson
from scipy.stats import norm
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
        "Trae Young", "Dejounte Murray", "De'Andre Hunter", "Bogdan Bogdanovic", "Clint Capela",
        "Jrue Holiday", "Derrick White", "Jaylen Brown", "Jayson Tatum", "Kristaps Porzingis",
        "Dennis Schroder", "Cam Thomas", "Mikal Bridges", "Cameron Johnson", "Nic Claxton",
        "Vasilije Micic", "Tre Mann", "Brandon Miller", "Miles Bridges", "Nick Richards",
        "Coby White", "Alex Caruso", "Ayo Dosunmu", "DeMar DeRozan", "Nikola Vucevic",
        "Darius Garland", "Donovan Mitchell", "Max Strus", "Evan Mobley", "Jarrett Allen",
        "Luka Doncic", "Kyrie Irving", "Derrick Jones Jr.", "P.J. Washington", "Daniel Gafford",
        "Jamal Murray", "Kentavious Caldwell-Pope", "Michael Porter Jr.", "Aaron Gordon", "Nikola Jokic",
        "Cade Cunningham", "Jaden Ivey", "Jaden Ivey", "Jaden Ivey", "Jalen Duren",
        "Stephen Curry", "Klay Thompson", "Andrew Wiggins", "Draymond Green", "Jonathan Kuminga",
        "Fred VanVleet", "Jalen Green", "Dillon Brooks", "Jabari Smith Jr.", "Amen Thompson",
        "Tyrese Haliburton", "Andrew Nembhard", "Aaron Nesmith", "Pascal Siakam", "Myles Turner",
        "Russell Westbrook", "James Harden", "Paul George", "Kawhi Leonard", "Ivica Zubac",
        "D'Angelo Russell", "Austin Reaves", "Rui Hachimura", "LeBron James", "Anthony Davis",
        "Scotty Pippen Jr.", "Desmond Bane", "Luke Kennard", "Jaren Jackson Jr.", "Santi Aldama",
        "Terry Rozier", "Tyler Herro", "Jimmy Butler", "Nikola Jovic", "Bam Adebayo",
        "Damian Lillard", "Malik Beasley", "Khris Middleton", "Giannis Antetokounmpo", "Brook Lopez",
        "Mike Conley", "Anthony Edwards", "Jaden McDaniels", "Naz Reid", "Rudy Gobert",
        "CJ McCollum", "Herbert Jones", "Trey Murphy III", "Zion Williamson", "Jonas Valanciunas",
        "Jalen Brunson", "Quentin Grimes", "RJ Barrett", "Julius Randle", "Mitchell Robinson",
        "Shai Gilgeous-Alexander", "Josh Giddey", "Jalen Williams", "Luguentz Dort", "Chet Holmgren",
        "Cole Anthony", "Jalen Suggs", "Franz Wagner", "Paolo Banchero", "Wendell Carter Jr.",
        "Tyrese Maxey", "Kyle Lowry", "Tobias Harris", "Kelly Oubre Jr.", "Mo Bamba",
        "Bradley Beal", "Devin Booker", "Grayson Allen", "Kevin Durant", "Jusuf Nurkic",
        "Scoot Henderson", "Anfernee Simons", "Kris Murray", "Jabari Walker", "Deandre Ayton",
        "De'Aaron Fox", "Kevin Huerter", "Harrison Barnes", "Keegan Murray", "Domantas Sabonis",
        "Malaki Branham", "Julian Champagnie", "Tre Jones", "Cedi Osman", "Victor Wembanyama",
        "Immanuel Quickley", "Gary Trent Jr.", "Gradey Dick", "RJ Barrett", "Kelly Olynyk",
        "Talen Horton-Tucker", "Jordan Clarkson", "Lauri Markkanen", "John Collins", "Walker Kessler",
        "Tyus Jones", "Jordan Poole", "Deni Avdija", "Kyle Kuzma", "Marvin Bagley III"
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
        player_pts_sd = player_stats["PTS"].std()
        player_avg_FG3M = round(player_stats["FG3M"].mean(),2)
        player_FG3M_sd = player_stats["FG3M"].std()
        player_avg_REB = round(player_stats["REB"].mean(),2)
        player_REB_sd = player_stats["REB"].std()
        player_avg_AST = round(player_stats["AST"].mean(),2)
        player_AST_sd = player_stats["AST"].std()
        
        
        #player_std_pts = player_stats["PTS"].std()
        #player_std_pts = player_stats["PTS"].std()
        #player_std_pts = player_stats["PTS"].std()
        #player_std_pts = player_stats["PTS"].std()
        
        
        #print(player_avg_pts)
        #print(player_avg_FG3M)
        #print(player_avg_REB)
        #print(player_avg_AST)
        
        
        
        for i in [10, 15, 20, 25, 30]:
            prob = 1 - norm.cdf(i-1, player_avg_pts,player_pts_sd)
            #print(prob)
            if prob < 0.1:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
        for i in [1,2,3,4,5]:
            prob = 1 - norm.cdf(i-1, player_avg_FG3M,player_FG3M_sd)
            #print(prob)
            if prob < 0.1:
                odds_list.append("0")
                probs_list.append("0")
                
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
                #print("through here")
        for i in [4,6,8,10,12,14,16]:
            prob = 1 - norm.cdf(i-1, player_avg_REB,player_REB_sd)
            if prob < 0.1:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
        for i in [2,4,6,8,10,12]:
            prob = 1 - norm.cdf(i-1, player_avg_AST,player_AST_sd)
            if prob < 0.1:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
            
            
    #print(odds_list)
    #print(len(odds_list))
    
    #print(probs_list)
    #print(len(probs_list))
        
    # Reshape the odds_list into a 5x24 DataFrame
    odds_df = pd.DataFrame(np.reshape(odds_list, (5, 23)), columns=bet_kinds)
    extended_df = pd.concat([team_df.reset_index(drop=True), odds_df], axis=1)
    print(extended_df)
    extended_df.to_csv("bet_stamps.csv",index=False)
        
    return extended_df
        
    
def gameOdds(game):
    
    away_team,home_team = game.split(' @ ')
    away_df = quickTeamOdds(away_team,"away")
    home_df = quickTeamOdds(home_team,"home")
                            
    game_df = pd.concat([away_df, home_df], ignore_index=True)
    #print(game_df)
    current_date = datetime.datetime.now().strftime("%m-%d-%Y")
    filename = f"{game}_{current_date}.csv"
    
    game_df.to_csv(f"computed_odds/{filename}", index=False)

    
'''
Notes:
    
    - Make all printing to a foldered file
    - SQL / Lin Reg

'''
    