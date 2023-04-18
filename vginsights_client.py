import logging
import time
import requests

class VGInsightsClient:
    @staticmethod
    def parse_game_stats(game_stats: object):
        return {
            "Title"	: game_stats['name'],
            "Release Date": game_stats['released'],
            "Price": game_stats['price'],
            "Rating": game_stats['rating'],
            "Gross Revenue": game_stats['revenue_vgi'],
            "Units Sold": game_stats['units_sold_vgi'],
            "Average Play Time": game_stats['avg_playtime'],
            "Company":game_stats["developers"],
            "Link": f"https://vginsights.com/game/{game_stats['steam_id']}",
        }
    
    @staticmethod
    def get_game_stats_by_id(game_id: str):
        time.sleep(.25)
        logging.info(f"Getting game stats: {game_id}")
        response = requests.get(
            f'https://vginsights.com/api/v1/game/{game_id}', 
            headers={
                'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://vginsights.com/game/331480',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                'sec-ch-ua-platform': '"Windows"',
            }
        )
        
        if not response.ok:
            logging.info(f"Throwing out bad response")
            return None
        
        try:
            base_data = response.json()
        except:
            logging.info(f"Throwing out bad response")
            return None

        response = requests.get(
            f'https://vginsights.com/api/v1/game/{game_id}/quick-stats', 
            headers= {
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://vginsights.com/game/810040',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            }
        )
        
        if not response.ok:
            logging.info(f"Throwing out bad response")
            return None

        return {
            **base_data,
            **response.json()
        }

    @staticmethod
    def get_game_ids(game_name: str):
        response = requests.get(
            'https://vginsights.com/api/v1/site-search', 
            params={
                'q': game_name,
            }, 
            headers={
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://vginsights.com/game/810040',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            }
        )
        if not response.ok:
            logging.error(response.text)
            raise Exception("Something went wrong")
        
        results = response.json()

        if len(results) == 0:
            return []
        elif len(results) == 1:
            return [results[0]['id']]
        return list(map(lambda x: x['id'], results))

    @staticmethod
    def get_game_stats_by_name(game_name: str):
        game_ids = VGInsightsClient.get_game_ids(game_name=game_name)
        return list(map(lambda game_id: VGInsightsClient.get_game_stats_by_id(game_id=game_id), game_ids))