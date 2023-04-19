from helpers import save_to_file, search_for_games_on_steam
from steam_client import SteamClient
from vginsights_client import VGInsightsClient

tags = ["rogue-like", "rogue-lite", "dungeon crawler"]

if __name__ == "__main__":
    for tag in tags:
        data = search_for_games_on_steam(tag=tag)
        # remove all games that were unable to load on the stat website
        game_stats = list(filter(lambda x: len(dict.keys(x)) > 1, data))
        # parse the results so we can import them into google sheet
        parsed_stats = list(map(VGInsightsClient.parse_game_stats, game_stats))
        # save data as a csv
        save_to_file(parsed_stats, file_type="csv", file_name=tag)

    