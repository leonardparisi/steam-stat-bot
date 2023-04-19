import requests

class VGInsightsClient:
    @staticmethod
    def parse_game_stats(game_stats: object):
        """ parse the stats to a nicer looking object for ease of use """
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
        """ gets stats for a game with the given ID """
        print(f"Getting game stats: {game_id}")

        # first get core stats
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
            print(f"Failed to fetch: {game_id}")
            return None
        
        try:
            base_data = response.json()
        except:
            print(f"Failed to fetch: {game_id}")
            return None

        # then fetch 'quick-stats' (i.e. revenue)
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
            print(f"Failed to fetch: {game_id}")
            return None

        return {
            **base_data,
            **response.json()
        }