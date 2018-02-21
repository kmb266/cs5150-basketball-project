import json, datetime, glob
import espn.espn_scraper as espn
from progress_bar import printProgressBar

cached_json = 'cached_json'
league = 'ncb'
playbyplay_folder_name = 'playbyplay'
start_yr = 2017

game_files = [filename for filename in glob.iglob('{}/{}/{}/*'.format(cached_json, league, playbyplay_folder_name))]

def scrape_players_from_pbp(pbp_json):
    players = {}
    for team in pbp_json['gamepackageJSON']['boxscore']['players']:
        print(team['statistics'][0]['athletes'][0])
        for player in team['statistics'][0]['athletes']:
            p_id = player['athlete']['id']
            p_name = player['athlete']['displayName']
            players[p_id] = p_name
    return players

def scrape_all_players():
    all_players = {}
    printProgressBar(0, len(game_files), prefix = '{} Player Scraping Progress:'.format(start_yr), suffix = 'Complete', length = 50)
    for i,game_file in enumerate(game_files):
        with open(game_file, 'r') as f:
            pbp_json = json.load(f)
            # single_game_players = scrape_players_from_pbp(pbp_json)
            for team in pbp_json['gamepackageJSON']['boxscore']['players']:
                team_info = team['team']
                for player in team['statistics'][0]['athletes']:
                    p_id = player['athlete']['id']
                    p_name = player['athlete']['displayName']
                    if '- Team' not in p_name and p_name != '-' and p_name != '- ':
                        all_players[p_id] = {'name':p_name, 'team': team_info['displayName']}
        printProgressBar(i+1, len(game_files), prefix = '{} Player Scraping Progress:'.format(start_yr), suffix = 'Complete', length = 50)
    return all_players
