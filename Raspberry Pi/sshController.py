import re

from commands import Commander

print("Initializing Pi...")

comm = Commander()

speed_matcher = re.compile("SPEED (\d+) (\d+) (\d+)")
move_matcher = re.compile("MOVE ([FBRLUS])")
distf_matcher = re.compile("DISTF")
distc_matcher = re.compile("DISTC")
noperson_matcher = re.compile("NOPERSON")
test_matcher = re.compile("TEST")
person_matcher = re.compile("PERSON (\d+)")

while True:
    command = input("Enter command:")

    if command.lower() == 's':
        print(f"Got: STOP")
        comm.move('S')
        continue

    if command.lower() == 'f':
        print(f"Got: F")
        comm.move('F')
        continue

    if command.lower() == 'b':
        print(f"Got: B")
        comm.move('B')
        continue

    if command.lower() == 'r':
        print(f"Got: R")
        comm.move('R')
        continue


    if command.lower() == 'l':
        print(f"Got: L")
        comm.move('L')
        continue


    if command.lower() == 'u':
        print(f"Got: U")
        comm.move('U')
        continue

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
    matched = distf_matcher.match(command)
    if (matched):
        print(f"Got: DISTF")
        dist = comm.getDistF()
        if (dist > 0):
            print(f"Distance read: {dist}")
        continue


    # DIST
    matched = distc_matcher.match(command)
    if (matched):
        print(f"Got: DISTC")
        dist = comm.getDistC()
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
        print(f"Got: PERSON {matched.group(1)}")
        comm.person(matched.group(1))
        continue  

    # TEST
    matched = test_matcher.match(command)
    if (matched):
        print(f"Got: TEST")
        print('Received ' + comm.test())
        continue

    matched = command.upper() == 'RON'
    if (matched):
        print(f"Got: RON")
        comm.ron()
        continue

    matched = command.upper() == 'ROFF'
    if (matched):
        print(f"Got: ROFF")
        comm.roff()
        continue

    matched = command.upper() == 'GON'
    if (matched):
        print(f"Got: GON")
        comm.gon()
        continue

    matched = command.upper() == 'GOFF'
    if (matched):
        print(f"Got: GOFF")
        comm.goff()
        continue

    matched = command.upper() == 'BON'
    if (matched):
        print(f"Got: BON")
        comm.bon()
        continue

    matched = command.upper() == 'BOFF'
    if (matched):
        print(f"Got: BOFF")
        comm.boff()
        continue

    matched = command.upper() == 'ON'
    if (matched):
        print(f"Got: ON")
        comm.ron()
        comm.gon()
        comm.bon()
        continue

    matched = command.upper() == 'OFF'
    if (matched):
        print(f"Got: OFF")
        comm.roff()
        comm.goff()
        comm.boff()
        continue

    matched = command.upper() == 'FLUSH'
    if (matched):
        print(f"Got: FLUSH")
        comm.flush()
        continue

    else:
        print("Command not recognized, stopping")
        comm.move('S')  
