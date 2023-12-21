#!/usr/bin/env python3
import requests, sys
from bs4 import BeautifulSoup

def get_game_pass_games(game_pass_url):
    try:
        response = requests.get(game_pass_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing Game Pass list: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    pc_games_header = soup.find('h2', id='PC')
    pc_games_list = pc_games_header and pc_games_header.find_next_sibling('ul')
    return [li.text.strip() for li in pc_games_list.find_all('li')] if pc_games_list else []

def get_steam_wishlist(url):
    wishlist_url = url.replace("#sort=order", "/wishlistdata/") if "#sort=order" in url else url + "/wishlistdata/"
    try:
        r = requests.get(wishlist_url, timeout=(3.05, 27))
        r.raise_for_status()
        wishlist = r.json()
    except requests.RequestException as e:
        print(f"Error loading Steam wishlist: {e}")
        sys.exit(1)

    return [item["name"] for item in wishlist.values()]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide your Steam wishlist URL.")
        sys.exit(1)

    wishlist_games = get_steam_wishlist(sys.argv[1])
    game_pass_games = get_game_pass_games("https://www.gamespot.com/articles/all-the-xbox-game-pass-games-right-now/1100-6448286")
    games_on_game_pass = [game for game in wishlist_games if game in game_pass_games]

    if games_on_game_pass:
        print("From this wishlist, these games are available on PC Game Pass:")
        print('\n'.join(games_on_game_pass))
    else:
        print("None of the games from the wishlist are currently available on PC Game Pass.")
