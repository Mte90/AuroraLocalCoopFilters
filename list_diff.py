#!/usr/bin/python3

file = open('./Coop4_.txt', 'r')
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