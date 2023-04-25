//
// Created by Leon Kabue on 3/25/23.
//

#include "rover.h"

void ROVER_initialize() {
    TIMER_SETUP();
    LEFT_init();
    RIGHT_init();
    ROVER_stop();
}

void ROVER_start(int speed) {
    ROVER_moveForward(speed);
}

void ROVER_moveForward(int speed){
    LEFT_forward(speed);
    RIGHT_forward(speed);
    ROVER_setMode(FORWARD_MODE);
}

void ROVER_moveBackward(int speed) {
    LEFT_backward(speed);
    RIGHT_backward(speed);
    ROVER_setMode(BACKWARD_MODE);
}

void ROVER_turnLeft(int speed) {
    LEFT_stop();
    RIGHT_forward(speed);
    ROVER_setMode(LEFT_MODE);
}

void ROVER_turnRight(int speed) {
    RIGHT_stop();
    LEFT_forward(speed);
    ROVER_setMode(RIGHT_MODE);
}

void ROVER_turnAround(int speed) {
    LEFT_forward(speed);
    RIGHT_backward(speed);
    ROVER_setMode(AROUND_MODE);
}

void ROVER_setSpeed(int speed1, int speed2) {
    LEFT_setSpeed(speed1);
    RIGHT_setSpeed(speed2);
}

void ROVER_increaseSpeed(int acc) {
    LEFT_increaseSpeed(acc);
    RIGHT_increaseSpeed(acc);
}

void ROVER_decreaseSpeed(int dec) {
    LEFT_decreaseSpeed(dec);
    RIGHT_decreaseSpeed(dec);
}

void ROVER_moveForward2(int speed_left, int speed_right) {
    LEFT_backward(speed_left);
    RIGHT_backward(speed_right);
    ROVER_setMode(FORWARD_MODE);
}

void ROVER_moveBackward2(int speed_left, int speed_right) {
    LEFT_backward(speed_left);
    RIGHT_backward(speed_right);
    ROVER_setMode(BACKWARD_MODE);
}

void ROVER_turnAround2(int speed_left, int speed_right) {
    LEFT_forward(speed_left);
    RIGHT_backward(speed_right);
    ROVER_setMode(AROUND_MODE);
}

void ROVER_stop() {
    LEFT_stop();
    RIGHT_stop();
    ROVER_setMode(STOP_MODE);
}

void ROVER_setMode(int mode) {
    MODE = mode;
}