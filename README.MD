# Steam Market Analysis Bot

### Overview 

This bot is meant to easily retrieve statistics on a wide selection of steam games in bulk.

## Setup

We need to install `NordVPN` so we can spoof locations. Then, install the python package `nordvpn-switcher` to control `NordVPN` from the script.

```
pip install nordvpn-switcher
```

## Usage

Here's an example snippet that gets all 'tower defense' games, parses the data, and saves it to a csv:

```python
from helpers import save_to_file, search_for_games_on_steam
from vginsights_client import VGInsightsClient

# search for all games with the tag 'tower defense' on steam
data = search_for_games_on_steam(tag="tower defense")
# remove all games that were unable to load on the stat website
game_stats = list(filter(lambda x: len(dict.keys(x)) > 1, data))
# parse the results so we can import them into google sheet
parsed_stats = list(map(VGInsightsClient.parse_game_stats, game_stats))
# save data as a csv
save_to_file(parsed_stats, file_type="csv")
```

The csv file should contain the following data:

```
Title,Release Date,Price,Rating,Gross Revenue,Units Sold,Average Play Time,Company,Link
ShawnCena121,2021-12-30T00:00:00.000Z,0.00,92.208,0,2310,,"Bifinley, Hirtha",https://vginsights.com/game/1835690
Neon Horizon:Eclipse,2021-12-21T00:00:00.000Z,6.99,100.000,907,180,,A13,https://vginsights.com/game/1835790
Amelie,2021-12-15T00:00:00.000Z,3.99,94.301,16784,5790,,Two and a Half Studios,https://vginsights.com/game/1835810
BetWin,2021-12-21T00:00:00.000Z,0.99,100.000,28,60,,Junhao,https://vginsights.com/game/1835820
Dead End Aegis,2022-01-14T00:00:00.000Z,29.99,93.750,21996,960,,metalogiq,https://vginsights.com/game/1835830
...
```
