# ESE 3500 Final Project
## Leon Kabue and Rafael Sakamoto
### Spring 23

## Overview

## Communication

The two systems communicate using UART through the USB ports. This ensures a reliable communication and already handles the level shifting necessary to interface between each other.

### Commands
#### From the Raspberry Pi:
- `SPEED <SPEED_L> <SPEED_R> <TIME>`<br>
    Instructs the Arduino to set the motor speeds to the given values for the given amount of time, in ms.<br>
    `<SPEED_L>` and `<SPEED_R>` Integers from 0 to 200, where 0 is reverse at full speed, and 200 is forward at full speed.

- `MOVE <DIR>`<br>
    Instructs the rover to move in the given direction.<br>
    `<DIR>` Valid directions are: `F` (forward), `B` (backward), `L` (left), `R` (right), `U` (turn around), `S` (stop)

- `DIST` <br>
    Requests the distance read by the Arduino.

- `NOPERSON` <br>
    Indicates that there is no person in sight
    
- `PERSON <ANGLE>`<br>
    Indicates that a victim was found at the given angle.<br>
    `<ANGLE>` Integer from 0 to 180, where 0 indicates a victim at 90 degrees to the left and 180 indicates one at 90 degrees to the right.

#### From the Arduino:
- `GOTDIST <DIST>` <br> 
    Returns the distance read.
- `DONE` <br>
    Indicates that the rover has finished a movement command.