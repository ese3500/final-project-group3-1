import re

from commands import Commander

print("Initializing Pi...")

comm = Commander()

speed_matcher = re.compile("SPEED (\d+) (\d+) (\d+)")
move_matcher = re.compile("MOVE ([FBRLUS])")
dist_matcher = re.compile("DIST")
noperson_matcher = re.compile("NOPERSON")
person_matcher = re.compile("PERSON (\d+)")

while True:
    command = input("Enter command:")

    # SPEED
    matched = speed_matcher.match(command)
    if (matched):
        print(f"Got: SPEED {matched.group(1)} {matched.group(2)} {matched.group(3)}")
        comm.setSpeed(matched.group(1), matched.group(2), matched.group(3))
        continue

    # MOVE
    matched = move_matcher.match(command)
    if (matched):
        print(f"Got: MOVE {matched.group(1)}")
        comm.move(matched.group(1))
        continue

    # DIST
    matched = dist_matcher.match(command)
    if (matched):
        print(f"Got: DIST")
        dist = comm.getDist()
        if (dist > 0):
            print(f"Distance read: {dist}")
        continue

    # NO PERSON
    matched = noperson_matcher.match(command)
    if (matched):
        print(f"Got: NOPERSON")
        comm.noPerson()
        continue

    # PERSON
    matched = person_matcher.match(command)
    if (matched):
        print(f"Got: NOPERSON {matched.group(1)}")
        comm.person(matched.group(1))
        continue    