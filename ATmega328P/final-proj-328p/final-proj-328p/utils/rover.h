//
// Created by Leon Kabue on 3/25/23.
//

#ifndef FINAL_ROVER_H
#define FINAL_ROVER_H

#include "motor.h"

typedef struct Mode{
    int mode;
} Mode;

static Mode m;

#define MODE m.mode

#define FORWARD_MODE 1
#define BACKWARD_MODE 2
#define LEFT_MODE 3
#define RIGHT_MODE 4
#define AROUND_MODE 5
#define STOP_MODE 6


void ROVER_initialize();

void ROVER_start(int speed);

void ROVER_moveForward(int speed);
void ROVER_moveBackward(int speed);

void ROVER_turnLeft(int speed);
void ROVER_turnRight(int speed);
void ROVER_turnAround(int speed);

void ROVER_setSpeed(int speed1, int speed2);
void ROVER_increaseSpeed(int acc);
void ROVER_decreaseSpeed(int dec);

void ROVER_stop();

void ROVER_setMode(int mode);

#endif //FINAL_ROVER_H
