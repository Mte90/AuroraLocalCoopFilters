#!/usr/bin/python3

# This is an hacky script used to generated the manual_*.txt files
# Let you compare some files with just TitleID and generate a list with the one missings

file = open('./Coop4.txt', 'r')
Lines = file.readlines()
ids = []
for line in Lines:
    ids.append(line.strip())

file = open('./Coop4.lua', 'r')
Lines = file.readlines()
checkids = []
for line in Lines:
    checkids.append(line.strip())

for maybeme in checkids:
    if maybeme not in ids:
        print(maybeme)
