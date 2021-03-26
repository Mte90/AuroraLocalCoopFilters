#!/usr/bin/python3

import csv
import json


def sanitize(game):
    game = game.lower().replace(':', ' ').replace(', the', '').replace('the', '').replace('*', '').replace("'", '')
    game = game.replace('ult.', 'ultimate').replace('tcs', 'tom clancys').replace('lotr', 'lord of rings')
    game = game.replace('rainbow six', 'rainbowsix').replace('acme arsenal', 'aa').replace('dynasty warriors', 'dw')
    game = game.replace('insect armageddon', 'ia').replace('original trilogy', '')
    game = game.replace('original adventures', '').replace('adventure continues', '')
    game = game.replace('clone wars', '').replace('vegas 2', 'vegas2').replace('world at war', 'waw')
    game = game.replace('science of evil', 'tsoe').replace('rise of cobra', '').replace('tom clancys', '')
    return game.replace('  ', ' ').replace('  ', ' ').replace('dw gundam', 'dwgundam').strip()


game_list = []
with open('./tmp/wiki.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if "XB360" in row[1]:
            line_count += 1
            game_list.append(row)
print(f'Found {line_count} Xbox 360 games.')

coop2 = []
coop4 = []
todefine = []
for row in game_list:
    coop = row[5]
    title = row[0]
    # Players number sanitization
    players = row[4].replace('*', '').replace('(?)', '').replace('?', '')
    if "-" in players:
        players = players.split('-')
        players = players[1]
    if "/" in players:
        players = players.split('/')
        players = players[1]
    if "," in players:
        players = players.split(',')
        players = players[0]
    if players == '':
        todefine.append(title)
        continue
    players = int(players)
    if "Local" in coop:
        if players == 2:
            coop2.append(sanitize(title))
        elif players >= 3:
            coop4.append(sanitize(title))
    # For future here the check if online

print('Found %d 2 Coop games.' % len(coop2))
print('Found %d 4+ Coop games.' % len(coop4))
print('%d games to manually define.' % len(todefine))

with open('titlecache.list') as f:
    titles = json.load(f)

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
        if title in game:
            titleId_coop2.append(game['titleid'])
            coop2.remove(game_name)

for title in coop4:
    for game in titles:
        game_name = sanitize(game['title'])
        if title in game:
            titleId_coop4.append(game['titleid'])
            coop4.remove(game_name)

with open('./tmp/wiki_2.txt', 'w') as f:
    f.write("\n".join(titleId_coop2))

with open('./tmp/wiki_4.txt', 'w') as f:
    f.write("\n".join(titleId_coop4))

print('%d 2 Coop games not identified.' % len(coop2))
print('%d 4+ Coop games not identified.' % len(coop4))