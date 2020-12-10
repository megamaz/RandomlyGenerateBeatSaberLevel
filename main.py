import json, pathlib, random, os
import msvcrt as m

try:
    with open('settings.json', 'r') as getSett:
        settings = json.load(getSett)
except FileNotFoundError:
    with open('settings.json', 'w') as makeSet:
        settings = {
            "songPath":"INSERT PATH HERE",
            "npb":2,
            "length":100,
            "nob":1
        }
        json.dump(settings, makeSet)

    with open("README.txt", 'w') as makeRead:
        makeRead.write("""Hey there, I'm here to make your life miserable.
Along with this file, a settings.json should have opened. if it didn't then something fucked up idk, contact me on discord megamaz#1020

Anyways, here's how the file works;
- songPath
The path to the song you want to randomly generate. Include .dat it can't guess what map you want

- npb
Notes Per Beat. how many notes there should be between beats. (if 2, there's gonna be 1 note every half beat. Floats do work if you want to make it wait more than 1 beat.)

- length
The length (in beat) of your song. That is calculated through bpm*(length of song in seconds)

- nob
Note On Beat. How many notes should appear in a single beat. (if you put 5, 5 notes will come at you and fucking kill you at the same time.)

I suggest playing those with no arrow, that way it's actually possible. but honestly idfc""")
    print("script has been setup. press any key to quit")
    m.getch()
    quit()
except Exception as unknown:
    print("Unknown error occured: {}".format(unknown))
    m.getch()

if not os.path.exists(settings["songPath"]):
    print("That song file doesn't exist. Put full path to level and include .dat")
    print("\npress any key to quit")
    m.getch()
    quit()
    # raise FileNotFoundError("That song file doesn't exist. Put full path to level and include .dat")
path = pathlib.Path(settings["songPath"])

with open(path, 'r') as loadLevel:
    level = json.load(loadLevel)

with open(path, 'w')  as generate:
    notes = []
    for i in range(int(settings["npb"]), int(settings["length"]*settings["npb"])): # starts later to prevent hot start to prevent hot start
        for b in range(settings["nob"]):
            note = {
                "_time":i*(1/settings["npb"]),
                "_lineIndex":random.randint(0, 3),
                "_lineLayer":random.randint(0, 2),
                "_type":random.randint(0,1),
                "_cutDirection":random.randint(0, 8)
            }
            notes.append(note)
    level["_notes"] = notes
    json.dump(level, generate)

print("Level has been generated.")
m.getch()