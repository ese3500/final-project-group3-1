# ESE 3500 Spring 23 Final Project
## Leon Kabue and Rafael Sakamoto

[Devpost Link](https://devpost.com/software/532295) <br>
[Demo video](https://youtu.be/BgxkRdhByj0)

## Overview
The recent natural disasters in Turkey and Syria shocked all of us in the past weeks. As engineers, that got us thinking about how we could potentially help in such scenarios. 
Our project seeks to help by making a small rover equipped with a thermal camera to identify the victims in difficult scenarios and send their coordinates to rescuers. We would use machine learning to differentiate heat signatures from humans to other sources and use pose detection to help guide our robot.
During our project, we encountered many challenges throughout the system, including building a reliable model with low resolution, noise, low refresh rate, and other limitations of the thermal camera. Nonetheless, we believe that, given the technical constraints, we were successfully able to demonstrate the potential of the system while also leaving room for future developments.

## How to run

The code is divided into two folders: the _ATMega328P_ folder contains the Microchip Studio project code for the code on the 328P, which interprets the UART commands described below and acts accordingly. The _Raspberry Pi_ folder contains the code on the Pi, and many test and other programs used throughout the development of the project. The main code used during the demo is `demo1.py`. 

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

- `DISTC` <br>
    Requests the distance of the short range sensor read by the Arduino.
    
- `DISTF` <br>
    Requests the distance of the long range sensor read by the Arduino.
    
- `RON` <br>
    Turns on the red LED    
    
- `ROFF` <br>
    Turns off the red LED    
    
- `GON` <br>
    Turns on the green LED    
    
- `GOFF` <br>
    Turns off the green LED
    
- `BON` <br>
    Turns on the blue LED    
    
- `BOFF` <br>
    Turns off the blue LED
