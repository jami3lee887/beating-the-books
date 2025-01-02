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

# 'Team': ["Atlanta Hawks"] * 9 + ["Boston Celtics"] * 9 + ["Brooklyn Nets"] * 9 + ["Charlotte Hornets"] * 9 +
#         ["Chicago Bulls"] * 9 + ["Cleveland Cavaliers"] * 9 + ["Dallas Mavericks"] * 9 + ["Denver Nuggets"] * 9 +
#         ["Detroit Pistons"] * 9 + ["Golden State Warriors"] * 9 + ["Houston Rockets"] * 9 + ["Indiana Pacers"] * 9 +
#         ["Los Angeles Clippers"] * 9 + ["Los Angeles Lakers"] * 9 + ["Memphis Grizzlies"] * 9 + ["Miami Heat"] * 9 +
#         ["Milwaukee Bucks"] * 9 + ["Minnesota Timberwolves"] * 9 + ["New Orleans Pelicans"] * 9 +
#         ["New York Knicks"] * 9 + ["Oklahoma City Thunder"] * 9 + ["Orlando Magic"] * 9 + ["Philadelphia 76ers"] * 9 +
#         ["Phoenix Suns"] * 9 + ["Portland Trail Blazers"] * 9 + ["Sacramento Kings"] * 9 + ["San Antonio Spurs"] * 9 +
#         ["Toronto Raptors"] * 9 + ["Utah Jazz"] * 9 + ["Washington Wizards"] * 9,

# Your data organized into a dictionary
starters_data = {
    'Team': ["Hawks"] * 9 + ["Celtics"] * 9 + ["Nets"] * 9 + ["Hornets"] * 9 +
            ["Bulls"] * 9 + ["Cavaliers"] * 9 + ["Mavericks"] * 9 + ["Nuggets"] * 9 +
            ["Pistons"] * 9 + ["Warriors"] * 9 + ["Rockets"] * 9 + ["Pacers"] * 9 +
            ["Clippers"] * 9 + ["Lakers"] * 9 + ["Grizzlies"] * 9 + ["Heat"] * 9 +
            ["Bucks"] * 9 + ["Timberwolves"] * 9 + ["Pelicans"] * 9 +
            ["Knicks"] * 9 + ["Thunder"] * 9 + ["Magic"] * 9 + ["76ers"] * 9 +
            ["Suns"] * 9 + ["Trail Blazers"] * 9 + ["Kings"] * 9 + ["Spurs"] * 9 +
            ["Raptors"] * 9 + ["Jazz"] * 9 + ["Wizards"] * 9,
    'Player': [
        "Jalen Johnson", "Jalen Johnson", "Clint Capela", "Trae Young", "Dyson Daniels", "Onyeka Okongwu", "Garrison Mathews", "De'Andre Hunter", "David Roddy",
        "Jrue Holiday", "Derrick White", "Jaylen Brown", "Jayson Tatum", "Al Horford", "Luke Kornet", "Payton Pritchard", "Kristaps Porzingis", "Xavier Tillman", 
        "Dennis Schroder", "Cam Thomas", "Ben Simmons", "Cameron Johnson", "Nic Claxton", "Dorian Finney-Smith", "Noah Clowney", "Ziaire Williams", "Jalen Wilson",
        "LaMelo Ball", "Cody Martin", "Brandon Miller", "Miles Bridges", "Nick Richards", "Tre Mann", "Grant Williams", "Vasilije Micic", "Vasilije Micic",
        "Coby White", "Zach LaVine", "Nikola Vucevic", "Patrick Williams", "Josh Giddey", "Ayo Dosunmu", "Lonzo Ball", "Julian Phillips", "Jalen Smith",
        "Darius Garland", "Donovan Mitchell", "Dean Wade", "Evan Mobley", "Jarrett Allen", "Georges Niang", "Caris LeVert", "Isaac Okoro", "Ty Jerome",
        "Luka Doncic", "Kyrie Irving", "Klay Thompson", "P.J. Washington", "Daniel Gafford", "Dereck Lively II", "Maxi Kleber", "Naji Marshall", "Jaden Hardy",
        "Jamal Murray", "Christian Braun", "Michael Porter Jr.", "Aaron Gordon", "Nikola Jokic", "Russell Westbrook", "Julian Strawther", "Peyton Watson", "Dario Saric",
        "Tim Hardaway Jr.", "Tobias Harris", "Cade Cunningham", "Jaden Ivey", "Jalen Duren", "Malik Beasley", "Isaiah Stewart", "Simone Fontecchio", "Simone Fontecchio",
        "Stephen Curry", "Trayce Jackson-Davis", "Andrew Wiggins", "Draymond Green", "Jonathan Kuminga", "Buddy Hield", "Brandin Podziemski", "Kevon Looney", "Gary Payton II",
        "Fred VanVleet", "Jalen Green", "Dillon Brooks", "Jabari Smith Jr.", "Alperen Sengun", "Cam Whitmore", "Amen Thompson", "Tari Eason", "Jock Landale",
        "Tyrese Haliburton", "Andrew Nembhard", "Aaron Nesmith", "Pascal Siakam", "Myles Turner", "Obi Toppin", "Bennedict Mathurin", "T.J. McConnell", "Ben Sheppard",
        "Derrick Jones Jr.", "James Harden", "Norman Powell", "Terance Mann", "Ivica Zubac", "Kris Dunn", "Kris Dunn", "Kevin Porter Jr.", "Nicolas Batum",
        "D'Angelo Russell", "Austin Reaves", "Rui Hachimura", "LeBron James", "Anthony Davis", "Max Christie", "Max Christie", "Jaxson Hayes", "Gabe Vincent",
        "Marcus Smart", "Desmond Bane", "Desmond Bane", "Jaren Jackson Jr.", "Desmond Bane", "Santi Aldama", "Jake LaRavia", "Scotty Pippen Jr.", "Brandon Clarke",
        "Terry Rozier", "Tyler Herro", "Jimmy Butler", "Nikola Jovic", "Bam Adebayo", "Alec Burks", "Jaime Jaquez Jr.", "Haywood Highsmith", "Thomas Bryant",
        "Damian Lillard", "Taurean Prince", "Gary Trent Jr.", "Giannis Antetokounmpo", "Brook Lopez", "Bobby Portis", "Pat Connaughton", "AJ Green", "Delon Wright",
        "Mike Conley", "Anthony Edwards", "Jaden McDaniels", "Julius Randle", "Rudy Gobert", "Donte DiVincenzo", "Naz Reid", "Nickeil Alexander-Walker", "Joe Ingles",
        "CJ McCollum", "Herbert Jones", "Daniel Theis", "Brandon Ingram", "Zion Williamson", "Dejounte Murray", "Jordan Hawkins", "Bogdan Bogdanovic", "Javonte Green",
        "Karl-Anthony Towns", "Josh Hart", "Jalen Brunson", "OG Anunoby", "Mikal Bridges", "Cameron Payne", "Cameron Payne", "Jericho Sims", "Jericho Sims",
        "Shai Gilgeous-Alexander", "Aaron Wiggins", "Jalen Williams", "Luguentz Dort", "Chet Holmgren", "Isaiah Joe", "Alex Caruso", "Cason Wallace", "Isaiah Joe",
        "Kentavious Caldwell-Pope", "Jalen Suggs", "Franz Wagner", "Paolo Banchero", "Wendell Carter Jr.", "Anthony Black", "Jonathan Isaac", "Moritz Wagner", "Cole Anthony",
        "Tyrese Maxey", "Kyle Lowry", "Caleb Martin", "Kelly Oubre Jr.", "Andre Drummond", "Eric Gordon", "Paul George", "Joel Embiid", "Guerschon Yabusele",
        "Josh Okogie", "Devin Booker", "Tyus Jones", "Kevin Durant", "Jusuf Nurkic", "Royce O'Neale", "Damion Lee", "Monte Morris", "Mason Plumlee",
        "Toumani Camara", "Jerami Grant", "Anfernee Simons", "Deni Avdija", "Deandre Ayton", "Scoot Henderson", "Kris Murray", "Shaedon Sharpe", "Jabari Walker",
        "De'Aaron Fox", "Kevin Huerter", "DeMar DeRozan", "Keegan Murray", "Domantas Sabonis", "Malik Monk", "Trey Lyles", "Alex Len", "Malik Monk",
        "Chris Paul", "Julian Champagnie", "Harrison Barnes", "Jeremy Sochan", "Victor Wembanyama", "Keldon Johnson", "Keldon Johnson", "Tre Jones", "Zach Collins",
        "Scottie Barnes", "Ochai Agbaji", "Gradey Dick", "Jakob Poeltl", "Ochai Agbaji", "RJ Barrett", "Chris Boucher", "Chris Boucher", "Chris Boucher",
        "Lauri Markkanen", "Walker Kessler", "Keyonte George", "Taylor Hendricks", "Collin Sexton", "Collin Sexton", "Jordan Clarkson", "John Collins", "Brice Sensabaugh",
        "Bilal Coulibaly", "Jordan Poole", "Kyle Kuzma", "Malcolm Brogdon", "Kyle Kuzma", "Kyle Kuzma", "Corey Kispert", "Jonas Valanciunas", "Marvin Bagley III",
        #rookies to add: Dalton Knecht, Jaylen wells
    ]
}

# Create DataFrame
teams_n_players = pd.DataFrame(starters_data)
extended_df = pd.DataFrame(starters_data)


# ------- for finding info tags
# player_dict = players.get_players()
# player = [player for player in player_dict if player['full_name'].lower() == "jaden ivey"][0]
# player_id = player['id']
# gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = '2024')
# gamelog_player_df = gamelog_player.get_data_frames()[0]


def quickTeamOdds(team,homeOrAway,dataThing):
    team_df = teams_n_players[teams_n_players['Team'] == team]
    
    odds_list = []
    probs_list = []
    bet_kinds = ["4+ Rebs", "6+ Rebs"]
    
    
    #list of all players
    player_dict = dataThing
    
    for i in team_df['Player']:
        
        player = [player for player in player_dict if player['full_name'].lower() == i.lower()][0]
        player_id = player['id']
        
        
        gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = '2024')
        gamelog_player_df = gamelog_player.get_data_frames()[0]
        
        # SOME PLAYER SD'S are still 0. (identical values across all games). so, for the next while, we use last year SD
        
        # EDIT, NOW GOING BACK TO 2024 DATA
        # gamelog_player_2023 = playergamelog.PlayerGameLog(player_id=player_id, season = '2023')
        # gamelog_player_df_2023 = gamelog_player_2023.get_data_frames()[0]

        # TEMPORARILY NOT DOING TO GATHER DATA        
        # if homeOrAway.lower() == "home":
        #     player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('vs', case=False, na=False)]
        
        # if homeOrAway.lower() == "away":
        #     player_stats = gamelog_player_df[gamelog_player_df['MATCHUP'].str.contains('@', case=False, na=False)]
        
        player_stats = gamelog_player_df
        #player_stats_old = gamelog_player_df_2023
        

        player_avg_REB = round(player_stats["REB"].mean(),2)
        player_REB_sd = player_stats["REB"].std()
        #### SD correction if 0
        # if player_REB_sd == 0:
        #     player_REB_sd = player_stats_old["REB"].std()
        # ####

        for i in [4,6]:
            prob = 1 - norm.cdf(i-1, player_avg_REB,player_REB_sd)
            if prob < 0.1:
                odds_list.append("0")
                probs_list.append("0")
            else:
                odds_list.append(round(1/prob,2))
                probs_list.append(round(prob,2))


    # Reshape the odds_list into a 9x24 DataFrame
    odds_df = pd.DataFrame(np.reshape(odds_list, (9, 2)), columns=bet_kinds)
    extended_df = pd.concat([team_df.reset_index(drop=True), odds_df], axis=1)
    print(extended_df)
    #extended_df.to_csv("bet_stamps.csv",index=False)
        
    return extended_df
        
    
def gameOdds(game):
    #      gameOdds("Atlanta Hawks @ Milwaukee Bucks")
    
    away_team,home_team = game.split(' @ ')
    
    dataThing = players.get_players()
    
    away_df = quickTeamOdds(away_team,"away",dataThing)
    home_df = quickTeamOdds(home_team,"home",dataThing)
                            
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
    