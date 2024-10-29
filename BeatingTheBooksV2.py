# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 23:20:42 2024

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
    'Team': ["Atlanta Hawks"] * 9 + ["Boston Celtics"] * 9 + ["Brooklyn Nets"] * 9 + ["Charlotte Hornets"] * 9 +
            ["Chicago Bulls"] * 9 + ["Cleveland Cavaliers"] * 9 + ["Dallas Mavericks"] * 9 + ["Denver Nuggets"] * 9 +
            ["Detroit Pistons"] * 9 + ["Golden State Warriors"] * 9 + ["Houston Rockets"] * 9 + ["Indiana Pacers"] * 9 +
            ["Los Angeles Clippers"] * 9 + ["Los Angeles Lakers"] * 9 + ["Memphis Grizzlies"] * 9 + ["Miami Heat"] * 9 +
            ["Milwaukee Bucks"] * 9 + ["Minnesota Timberwolves"] * 9 + ["New Orleans Pelicans"] * 9 +
            ["New York Knicks"] * 9 + ["Oklahoma City Thunder"] * 9 + ["Orlando Magic"] * 9 + ["Philadelphia 76ers"] * 9 +
            ["Phoenix Suns"] * 9 + ["Portland Trail Blazers"] * 9 + ["Sacramento Kings"] * 9 + ["San Antonio Spurs"] * 9 +
            ["Toronto Raptors"] * 9 + ["Utah Jazz"] * 9 + ["Washington Wizards"] * 9,
    'Player': [
        "Jalen Johnson", "Jalen Johnson", "Clint Capela", "Trae Young", "Dyson Daniels", "Onyeka Okongwu", "Garrison Mathews", "Vit Krejci", "David Roddy",
        "Jrue Holiday", "Derrick White", "Jaylen Brown", "Jayson Tatum", "Al Horford", "Luke Kornet", "Payton Pritchard", "Xavier Tillman", "Xavier Tillman", 
        "Dennis Schroder", "Cam Thomas", "Ben Simmons", "Cameron Johnson", "Nic Claxton", "Dorian Finney-Smith", "Noah Clowney", "Ziaire Williams", "Jalen Wilson",
        "LaMelo Ball", "Cody Martin", "Seth Curry", "Miles Bridges", "Nick Richards", "Tre Mann", "Grant Williams", "Vasilije Micic", "Tidjane Salaun",
        "Coby White", "Zach LaVine", "Nikola Vucevic", "Patrick Williams", "Josh Giddey", "Ayo Dosunmu", "Lonzo Ball", "Julian Phillips", "Jalen Smith",
        "Darius Garland", "Donovan Mitchell", "Dean Wade", "Evan Mobley", "Jarrett Allen", "Georges Niang", "Sam Merrill", "Isaac Okoro", "Ty Jerome",
        "Luka Doncic", "Kyrie Irving", "Klay Thompson", "P.J. Washington", "Daniel Gafford", "Dereck Lively II", "Maxi Kleber", "Naji Marshall", "Jaden Hardy",
        "Jamal Murray", "Christian Braun", "Michael Porter Jr.", "Aaron Gordon", "Nikola Jokic", "Russell Westbrook", "Julian Strawther", "Peyton Watson", "Dario Saric",
        "Tim Hardaway Jr.", "Tobias Harris", "Cade Cunningham", "Jaden Ivey", "Jalen Duren", "Malik Beasley", "Isaiah Stewart", "Simone Fontecchio", "Simone Fontecchio",
        "Stephen Curry", "Trayce Jackson-Davis", "Andrew Wiggins", "Draymond Green", "Jonathan Kuminga", "Buddy Hield", "Brandin Podziemski", "Kevon Looney", "Gary Payton II",
        "Fred VanVleet", "Jalen Green", "Dillon Brooks", "Jabari Smith Jr.", "Alperen Sengun", "Cam Whitmore", "Amen Thompson", "Tari Eason", "Jock Landale",
        "Tyrese Haliburton", "Andrew Nembhard", "Aaron Nesmith", "Pascal Siakam", "Myles Turner", "Obi Toppin", "Bennedict Mathurin", "T.J. McConnell", "Ben Sheppard",
        "Derrick Jones Jr.", "James Harden", "Norman Powell", "Terance Mann", "Ivica Zubac", "Kris Dunn", "Amir Coffey", "Kevin Porter Jr.", "Nicolas Batum",
        "D'Angelo Russell", "Austin Reaves", "Rui Hachimura", "LeBron James", "Anthony Davis", "Dalton Knecht", "Max Christie", "Jaxson Hayes", "Gabe Vincent",
        "Marcus Smart", "Desmond Bane", "Zach Edey", "Jaren Jackson Jr.", "Desmond Bane", "Santi Aldama", "Jake LaRavia", "Scotty Pippen Jr.", "Brandon Clarke",
        "Terry Rozier", "Tyler Herro", "Jimmy Butler", "Nikola Jovic", "Bam Adebayo", "Alec Burks", "Jaime Jaquez Jr.", "Duncan Robinson", "Thomas Bryant",
        "Damian Lillard", "Taurean Prince", "Gary Trent Jr.", "Giannis Antetokounmpo", "Brook Lopez", "Bobby Portis", "Pat Connaughton", "AJ Green", "Delon Wright",
        "Mike Conley", "Anthony Edwards", "Jaden McDaniels", "Julius Randle", "Rudy Gobert", "Donte DiVincenzo", "Naz Reid", "Nickeil Alexander-Walker", "Joe Ingles",
        "CJ McCollum", "Herbert Jones", "Daniel Theis", "Brandon Ingram", "Zion Williamson", "Jordan Hawkins", "Yves Missi", "Jose Alvarado", "Javonte Green",
        "Karl-Anthony Towns", "Josh Hart", "Jalen Brunson", "OG Anunoby", "Mikal Bridges", "Cameron Payne", "Miles McBridge", "Jericho Sims", "Ariel Hukporti",
        "Shai Gilgeous-Alexander", "Aaron Wiggins", "Jalen Williams", "Luguentz Dort", "Chet Holmgren", "Cason Wallace", "Alex Caruso", "Isaias Joe", "Ajay Mithcell",
        "Kentavious Caldwell-Pope", "Jalen Suggs", "Franz Wagner", "Paolo Banchero", "Wendell Carter Jr.", "Anthony Black", "Jett Howard", "Moritz Wagner", "Cole Anthony",
        "Tyrese Maxey", "Kyle Lowry", "Caleb Martin", "Kelly Oubre Jr.", "Andre Drummond", "Eric Gordon", "Kenyon Martin Jr.", "Jared McCain", "Guerschon Yabusele",
        "Ryan Dunn", "Devin Booker", "Tyus Jones", "Kevin Durant", "Jusuf Nurkic", "Royce O'Neale", "Damion Lee", "Monte Morris", "Mason Plumlee",
        "Toumani Camara", "Jerami Grant", "Anfernee Simons", "Deni Avdija", "Deandre Ayton", "Scoot Henderson", "Kris Murray", "Jabari Walker", "Donovan Clingan",
        "De'Aaron Fox", "Kevin Huerter", "Harrison Barnes", "Keegan Murray", "Domantas Sabonis", "Malik Monk", "Trey Lyles", "Alex Len", "Jordan McLaughlin",
        "Chris Paul", "Julian Champagnie", "Harrison Barnes", "Jeremy Sochan", "Victor Wembanyama", "Keldon Johnson", "Stephon Johnson", "Tre Jones", "Zach Collins",
        "Scottie Barnes", "Ochai Agbaji", "Gradey Dick", "Jakob Poeltl", "Davion Mitchell", "Chris Boucher", "Chris Boucher", "Chris Boucher", "Bruno Fernando",
        "Lauri Markkanen", "Walker Kessler", "Keyonte George", "Taylor Hendricks", "Collin Sexton", "Cody Williams", "Jordan Clarkson", "John Collins", "Brice Sensabaugh",
        "Bilal Coulibaly", "Jordan Poole", "Kyle Kuzma", "Kyle Kuzma", "Kyle Kuzma", "Kyle Kuzma", "Corey Kispert", "Jonas Valanciunas", "Marvin Bagley III",
    ]
}

# Create DataFrame
teams_n_players = pd.DataFrame(starters_data)
extended_df = pd.DataFrame(starters_data)


# ------- for finding info tags
player_dict = players.get_players()
player = [player for player in player_dict if player['full_name'].lower() == "jaden ivey"][0]
player_id = player['id']
gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = '2024')
gamelog_player_df = gamelog_player.get_data_frames()[0]


def quickTeamOdds(team,homeOrAway):
    team_df = teams_n_players[teams_n_players['Team'] == team]
    
    odds_list = []
    probs_list = []
    bet_kinds = ["10+ PTS", "19+ PTS", "20+ PTS", "29+ PTS", "30+ PTS", "1+ 3's", "2+ 3's", "3+ 3's", "4+ 3's", "9+ 3's", 
                 "4+ Rebs", "6+ Rebs", "8+ Rebs", "10+ Rebs", "12+ Rebs", "14+ Rebs", "16+ Rebs",
                 "2+ ASTs", "4+ ASTs", "6+ ASTs", "8+ ASTs", "10+ ASTs", "12+ ASTs",]
    
    
    #list of all players
    player_dict = players.get_players()
    
    for i in team_df['Player']:
        
        player = [player for player in player_dict if player['full_name'].lower() == i.lower()][0]
        player_id = player['id']
        
        
        gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = '2024')
        gamelog_player_df = gamelog_player.get_data_frames()[0]
        
        # SOME PLAYER SD'S are still 0. (identical values across all games). so, for the next while, we use last year SD
        gamelog_player_2023 = playergamelog.PlayerGameLog(player_id=player_id, season = '2023')
        gamelog_player_df_2023 = gamelog_player_2023.get_data_frames()[0]

        # TEMPORARILY NOT DOING TO GATHER DATA        
        # if homeOrAway.lower() == "home":
        #     player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('vs', case=False, na=False)]
        
        # if homeOrAway.lower() == "away":
        #     player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('@', case=False, na=False)]
        player_stats = gamelog_player_df
        player_stats_old = gamelog_player_df_2023
        
        player_avg_pts = round(player_stats["PTS"].mean(),2)
        player_pts_sd = player_stats["PTS"].std()
        player_avg_FG3M = round(player_stats["FG3M"].mean(),2)
        player_FG3M_sd = player_stats["FG3M"].std()
        player_avg_REB = round(player_stats["REB"].mean(),2)
        player_REB_sd = player_stats["REB"].std()
        #### SD correction if 0
        if player_REB_sd == 0:
            player_REB_sd = player_stats_old["REB"].std()
        ####
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
        
        
        
        for i in [10, 19, 20, 29, 30]:
            prob = 1 - norm.cdf(i-1, player_avg_pts,player_pts_sd)
            #print(prob)
            if prob < 0.1:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))
        
        for i in [1,2,3,4,9]:
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
        
    # Reshape the odds_list into a 9x24 DataFrame
    odds_df = pd.DataFrame(np.reshape(odds_list, (9, 23)), columns=bet_kinds)
    extended_df = pd.concat([team_df.reset_index(drop=True), odds_df], axis=1)
    print(extended_df)
    #extended_df.to_csv("bet_stamps.csv",index=False)
        
    return extended_df
        
    
def gameOdds(game):
    
    away_team,home_team = game.split(' @ ')
    
    away_df = quickTeamOdds(away_team,"away")
    home_df = quickTeamOdds(home_team,"home")
                            
    game_df = pd.concat([away_df, home_df], ignore_index=True)
    #print(game_df)
    current_date = datetime.datetime.now().strftime("%m-%d-%Y")
    filename = f"{game}_{current_date}.csv"
    
    game_df.to_csv(f"computed_odds_2024/{filename}", index=False)

    
'''
Notes:
    
    - SQL / Lin Reg
    - sqlite the team city, when you pass in the team name

'''
    