import csv
import json
from typing import List
import random
import time
from steam_client import SteamClient
from vginsights_client import VGInsightsClient
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN

    
# search for all games on steam with the given tag and get information about each of them
def search_for_games_on_steam(tag: str, start: int = 0, end:int = None, vpn_switches:int = 60, min_delay: float=0.1, max_delay: float=10):
    # first get list of games
    games = SteamClient.get_games_by_tag(tag)
    
    # if 'end' is not specified, do the whole list of games 
    if end is None:
        end = len(games)-1
    # end early if we already finished going through the list of games 
    if end >= len(games):
        return
    
    # initialize the vpn and get a new IP
    initialize_VPN(save=1,area_input=['complete rotation'])
    rotate_VPN()

    # go through each game, look up stats for it, write results to 'raw.json' in case something breaks so we dont lose all the data
    game_stats = []
    for i in range(start, end):
        # we want to change locations every few games to avoid hitting spam detection mechanisms
        if i % vpn_switches == 0:
            print("Changing location...")
            rotate_VPN()

        # now get the stats for the game
        game = games[i]
        game_id = game['appid']
        results = VGInsightsClient.get_game_stats_by_id(game_id=game_id)

        # wait a random amount of time to help avoid getting flagged by bot detection right away
        print("Waiting...")
        time.sleep(random.uniform(min_delay, max_delay))

        # if no results were found, record the name and ID incase we want to know which games got skipped
        if results is None:
            results = { game['name']:game_id }
        # save the results
        game_stats.append(results)
        save_to_file(game_stats, file_type="json",file_name="raw")

    terminate_VPN()

def save_to_file(data: List[object], file_type: str='csv', file_name: str = "output"):
    if file_type == 'csv':
        with open(f'{file_name}.csv', 'w', newline='') as csv_file:
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                try:
                    writer.writerow(row)
                except:
                    continue

    elif file_type == 'json':
        with open(f'{file_name}.json', 'w') as f:
            json.dump(data, f, indent=5)