"""Is Artifact Dead? edit: yes"""

import os
import pickle
import time

from dotenv import load_dotenv
from flask import render_template
from steam.webapi import WebAPI  # type: ignore

from isitdead import app

GAMES_CACHE_FILENAME = "games.cache"
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))
STEAM_API_KEY = os.environ.get("STEAM_API_KEY")


def get_cache():
    """Grabs the cached data."""
    try:
        infile = open(GAMES_CACHE_FILENAME, "rb")
        new_games = pickle.load(infile)
        return new_games if use_cache(new_games) else update_and_get_cache()
    except FileNotFoundError:
        return update_and_get_cache()


def use_cache(cache):
    """Check to see if we use the cached data instead of downloading new."""
    return time.time() < cache["expire"]


def update_and_get_cache():
    """Download new data and update the cache with this new data."""
    games = update_counts()
    outfile = open(GAMES_CACHE_FILENAME, "wb")
    cache = {"expire": time.time() + 300, "games": games}
    pickle.dump(cache, outfile)
    outfile.close()
    return cache


class Game:  # pylint: disable=too-few-public-methods
    """The other card games on Steam I noticed."""

    def __init__(self, name, appid):
        self.appid = appid
        self.name = name
        self.players = 0

    def update(self, api):
        """Updates the player count for each of these games."""
        self.players = int(
            api.call("ISteamUserStats.GetNumberOfCurrentPlayers", appid=self.appid)[
                "response"
            ]["player_count"]
        )


def update_counts():
    """Update the player counts for each of the following gams."""
    gams = [
        ("Artifact Classic", 583950),
        ("Artifact Foundry", 1269260),
        ("Eternal", 531640),
        ("Yu-Gi-Oh! Duel Links", 601510),
        ("The Elder Scrolls: Legends", 364470),
        ("Shadowverse CCG", 453480),
        ("Yu-Gi-Oh! Master Duel", 1449850),
    ]
    games = list(map(lambda x: Game(x[0], x[1]), gams))

    api = WebAPI(STEAM_API_KEY)
    for game in games:
        game.update(api)
    return games


def top_five(games):
    """Print a pretty ascii art top 5."""
    top5 = f"""
   -yhdddddmmmmh` `ymmmdmmmmmmmmNNNNmmmmmmmmmd:   
    .hmmmmmNNNmN+  -NNMNMMMMNNNNNNNNNNNNmmmmh.      Player counts update every five minutes.
     `sdddmdmNNNd.  odmmNNNNNNNNNNNNNmmmmmmy`     
      `+dmdymmmmmo    `.-/+sydmmNNmymmddddo`         #1) {games[0].name}: {games[0].players}
        /hhddddmmd-  :+/-.``  `.:/+oyhhyh/        
         :yhddmdddo  .dNmmdhs/`  ```  `.-            #2) {games[1].name}: {games[1].players}
          -shhddddh-  //RIP//  .+hhyoo/`          
           .oyyshdds` `yds-  .+hhhhdyo.              #3) {games[2].name}: {games[2].players}
            `+yhhhhd/  --  -ohddhhhy+`            
             `/yyyhhs`   -oyyhhhyys/                 #4) {games[3].name}: {games[3].players}
               :sys+.  -oyyyyyysso-               
                -/.  -oyyyysssoo+.                   #5) {games[4].name}: {games[4].players}
                   -+osssssoooo/`                 
                  `/+++osooooo/`                     #6) {games[5].name}: {games[5].players}
                    -+ooooos+-                    
                     .++++so-                        #7) {games[6].name}: {games[6].players}
                      ./++/.                      
                       `::`                       
                        ``
"""
    return top5


@app.route("/")
def home():
    """The Only Route I Have"""
    games = get_cache()["games"]
    sorted_games = sorted(games, key=lambda x: x.players, reverse=True)

    classic_count = f"{games[0].players:,}"
    foundry_count = f"{games[1].players:,}"

    player_count = str(int(classic_count) + int(foundry_count))
    explain = f"{classic_count} classic + {foundry_count} foundry players"

    return render_template(
        "home.html",
        player_count=player_count,
        top5=top_five(sorted_games),
        explain=explain,
    )


if __name__ == "__main__":
    app.run()
