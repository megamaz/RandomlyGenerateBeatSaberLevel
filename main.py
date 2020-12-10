import json, pathlib, random, os
import msvcrt as m

version = "1.1.0" # this needs to match the on in the JSON file, so you can download new exe and you good 
def setup():
    with open('settings.json', 'w') as makeSet:
        settings = {
            "appVersion":"1.1.0",
            "songPath":"INSERT PATH HERE",
            "notePerBeat":2,
            "length":100,
            "notesOnBeat":1,
            "includeBombs":False,
            "checkDouble":False
        }
        json.dump(settings, makeSet)

    with open("README.txt", 'w') as makeRead:
        makeRead.write("""Hey there, I'm here to make your life miserable.
Along with this file, a settings.json should have opened. if it didn't then something fucked up idk, contact me on discord megamaz#1020
If you change the appVersion setting, this will reset your settings to default. 

Anyways, here's how the file works;
- songPath
The path to the song you want to randomly generate. Include .dat it can't guess what map you want

- notePerBeat
Notes Per Beat. how many notes there should be between beats. (if 2, there's gonna be 1 note every half beat. Floats do work if you want to make it wait more than 1 beat.)

- length
The length (in beat) of your song. That is calculated through bpm*(length of song in seconds)

- notesOnBeat
Note On Beat. How many notes should appear in a single beat. (if you put 5, 5 notes will come at you and fucking kill you at the same time.)

- includeBombs
if true, it includes bombs.

- checkDouble
Checks if a note is already in place before placing the note. (this prevents note stacking, or having two notes in the same slot.)
If this is true, then the noteOnBeat is limited to 12 (3x4) otherwise the program will never end.

I suggest playing those with no arrow, that way it's actually possible. but honestly idfc""")
    return settings
try:
    with open('settings.json', 'r') as getSett:
        settings = json.load(getSett)
except FileNotFoundError:
    settings = setup()
    print("script has been setup. press any key to quit")
    m.getch()
    quit()
except Exception as unknown:
    print("Unknown error occured: {}".format(unknown))
    m.getch()

if "appVersion" not in settings.keys():
    setup()
    print("Script has been updated. Press any key to quit.")
    m.getch()
    quit()

elif settings["appVersion"] != version:
    setup()
    print("Script has been updated. Press any key to quit.")
    m.getch()
    quit()

if settings["checkDouble"] and settings["notesOnBeat"] > 12:
    print("noteOnBeat being greater than 12 is incompatible with checkDouble")
    settings["notesOnBeat"] = 12
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
    for i in range(int(settings["notePerBeat"]), int(settings["length"]*settings["notePerBeat"])): # starts later to prevent hot start to prevent hot start
        poss = [ # This is a lazy fix. but fuck it.
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
            (3, 0),
            (3, 1),
            (3, 2)
        ]
        for _ in range(settings["notesOnBeat"]):
            if settings["includeBombs"]:
                noteType = random.randint(0,3)
                while noteType == 2: # 2 is a nothing. you don't want to include nothing. so i prevent nothing, giving you something.
                    noteType = random.randint(0,3) # making this a while loop gives 0, 1, and 3 the same chance of happening. 2 never happens.
            else:
                noteType = random.randint(0,1)
            pos = random.choice(poss)
            if settings["checkDouble"]:
                poss.remove(pos)
                print(poss)                 
            note = {
                "_time":i*(1/settings["notePerBeat"]),
                "_lineIndex":pos[0],
                "_lineLayer":pos[1],
                "_type":noteType,
                "_cutDirection":random.randint(0, 8)
            }
            notes.append(note)
    level["_notes"] = notes
    json.dump(level, generate)

print("Level has been generated. Press any key to quit.")
m.getch()