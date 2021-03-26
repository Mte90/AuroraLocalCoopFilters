#!/usr/bin/python3

# Based on https://github.com/CasulOrnstein/HackNotts-Choose-a-Game/blob/master/Data/scrapeCoopData.py
import requests
from bs4 import BeautifulSoup
import os
import json


def sanitize(game):
    game = game.lower().replace(':', ' ').replace('the', '').replace('*', '').replace("'", '')
    game = game.replace('tcs', '').replace('tom clancys', '').replace('lotr', 'lord of rings')
    return game.replace('  ', ' ').replace('  ', ' ').replace(' ', '').strip()


if not os.path.exists('./tmp/cooptimus_2_titles.txt'):
    coop2 = []
    coop4 = []

    for page in range(1, 27):
        print("%d page in parsing" % page)
        URL = f'https://www.co-optimus.com/ajax/ajax_games.php?game-title-filter=&system=1&countDirection=at%20least&playerCount=2&page={page}&sort=playersoffline&sortDirection=DESC'
        data = requests.get(URL)
        soup = BeautifulSoup(data.content, 'html.parser')
        rows = soup.find_all('tr')

        for row in rows:
            results = {}

            # Find the games name
            cells = row.find_all('td')
            if cells:
                if cells[2]:
                    players = int(cells[2].text)
                    if cells[0]:
                        strong = cells[0].find('strong')
                        text = sanitize(strong.text)
                        if players == 2:
                            coop2.append(text)
                        elif players >= 3:
                            coop4.append(text)

    with open('./tmp/cooptimus_2_titles.txt', 'w') as f:
        f.write("\n".join(coop2))

    with open('./tmp/cooptimus_4_titles.txt', 'w') as f:
        f.write("\n".join(coop4))

coop2 = []
coop4 = []
file = open('./tmp/cooptimus_2_titles.txt', 'r')
Lines = file.readlines()
for line in Lines:
    coop2.append(line.strip())

file = open('./tmp/cooptimus_4_titles.txt', 'r')
Lines = file.readlines()
for line in Lines:
    coop4.append(line.strip())

with open('titlecache.list') as f:
    titles = json.load(f)

print('Found %d 2 Coop games.' % len(coop2))
print('Found %d 4+ Coop games.' % len(coop4))

titleId_coop2 = []
titleId_coop4 = []

for game in titles:
    game_name = sanitize(game['title'])
    if game_name in coop2:
        titleId_coop2.append(game['titleid'])
        coop2.remove(game_name)
    if game_name in coop4:
        titleId_coop4.append(game['titleid'])
        coop4.remove(game_name)

for title in coop2:
    for game in titles:
        game_name = sanitize(game['title'])
        if title in game['title']:
            titleId_coop2.append(game['titleid'])
            try:
                coop2.remove(title)
            except:
                pass

for title in coop4:
    for game in titles:
        game_name = sanitize(game['title'])
        if title in game['title']:
            titleId_coop4.append(game['titleid'])
            coop4.remove(game_name)

with open('./tmp/cooptimus_2.txt', 'w') as f:
    f.write("\n".join(titleId_coop2))

with open('./tmp/cooptimus_4.txt', 'w') as f:
    f.write("\n".join(titleId_coop4))

with open('./tmp/cooptimus_2_titles_missing.txt', 'w') as f:
    f.write("\n".join(coop2))

with open('./tmp/cooptimus_4_titles_missing.txt', 'w') as f:
    f.write("\n".join(coop4))

print('%d 2 Coop games not identified.' % len(coop2))
print('%d 4+ Coop games not identified.' % len(coop4))