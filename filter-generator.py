#!/usr/bin/python3

def merge_files(players):
    file = open('./tmp/wiki_' + str(players) + '.txt', 'r')
    Lines = file.readlines()
    ids = []
    for line in Lines:
        ids.append(line.strip())

    file = open('./manual_' + str(players) + '.txt', 'r')
    Lines = file.readlines()
    for line in Lines:
        ids.append(line.strip())

    file = open('./tmp/cooptimus_' + str(players) + '.txt', 'r')
    Lines = file.readlines()
    for line in Lines:
        ids.append(line.strip())

    ids = list(dict.fromkeys(ids))

    print('For %d players we found %d games.' % (players, len(ids)))

    return ids


def generate_lua(players):
    count = 0
    temp = ""
    for titleid in merge_files(players):
        count += 1
        if count == 1:
            temp += "\nreturn (Content.TitleId == 0x" + titleid
        else:
            temp += "\nor Content.TitleId == 0x" + titleid

    temp += ")\nend"
    return temp


boilerplate = 'GameListFilterCategories.User["CHANGEME"] = function(Content)'

# 2 players

lua2 = boilerplate.replace('CHANGEME', 'Local Co-op 2 Players')
lua2 += generate_lua(2)
lua = open("Coop2.lua", "w")
lua.write(lua2)
lua.close()

# 4 players

lua4 = boilerplate.replace('CHANGEME', 'Local Co-op 4+ Players')
lua4 += generate_lua(4)
lua = open("Coop4.lua", "w")
lua.write(lua4)
lua.close()