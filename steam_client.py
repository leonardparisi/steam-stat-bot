from typing import List
import requests


class SteamClient:
    @staticmethod
    def get_games_by_tag(tag: str) -> List[str]:
        """ get all steam games with the given tag """
        steam_games = requests.get(
                "http://api.steampowered.com/ISteamApps/GetAppList/v0002/", 
                                    params={
                "tag":tag
            }
        ).json()
        return list(filter(lambda x: x['name'] != "" and "test" not in x['name'], steam_games['applist']['apps']))
    
    @staticmethod
    def get_games_with_substring(substring: str) -> List[str]:
        """ get all steam games with the substring in the name """
        steam_games = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json").json()
        return list(filter( lambda x: substring in x['name'].lower(), steam_games['applist']['apps']))