import json
import csv
import logging
from typing import List

import requests
from vginsights_client import VGInsightsClient

def flatten(l):
    return [item for sublist in l for item in sublist]

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
    

def get_all_game_stats_and_save():
    # set log level
    logging.basicConfig(level = logging.INFO)
    # open the inputs file
    f = open('inputs.json')
    data = json.load(f)
    # then loop through all the games and find stats on them
    game_stats = flatten(list(map(VGInsightsClient.get_game_stats_by_name, data['games'])))
    # parse the stats
    parsed_stats = list(map(VGInsightsClient.parse_game_stats, game_stats))
    # save stats to a file
    save_to_file(parsed_stats, file_type="csv")
    save_to_file(parsed_stats, file_type="json")

def search_for_games_on_steam(title_includes: str):
    steam_games = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json").json()
    games = list(map(lambda x: x['appid'], filter( lambda x: title_includes in x['name'].lower(), steam_games['applist']['apps'])))
    game_stats = list(filter(lambda x: x is not None, map(VGInsightsClient.get_game_stats_by_id, games)))
    save_to_file(game_stats, file_type="json",file_name="unparsed_output")
    return game_stats

if __name__ == "__main__":
    get_all_game_stats_and_save()