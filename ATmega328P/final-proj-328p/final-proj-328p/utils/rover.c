//
// Created by Leon Kabue on 3/25/23.
//

#include "rover.h"

void ROVER_initialize() {
    TIMER1_SETUP();
    MOTOR1_init();
    MOTOR2_init();
    ROVER_stop();
}

void ROVER_start(int speed) {
    ROVER_moveForward(speed);
}

void ROVER_moveForward(int speed){
    ROVER_setSpeed(speed, speed);
    MOTOR1_forward();
    MOTOR2_forward();
    ROVER_setMode(FORWARD_MODE);
}

void ROVER_moveBackward(int speed) {
    ROVER_setSpeed(speed, speed);
    MOTOR1_backward();
    MOTOR2_backward();
    ROVER_setMode(BACKWARD_MODE);
}

void ROVER_turnLeft(int speed) {
    ROVER_setSpeed(speed, speed);
    MOTOR2_stop();
    MOTOR1_forward();
    ROVER_setMode(LEFT_MODE);
}

void ROVER_turnRight(int speed) {
    ROVER_setSpeed(speed, speed);
    MOTOR1_stop();
    MOTOR2_forward();
    ROVER_setMode(RIGHT_MODE);
}

void ROVER_turnAround(int speed) {
    ROVER_setSpeed(speed, speed);
    MOTOR1_forward();
    MOTOR2_backward();
    ROVER_setMode(AROUND_MODE);
}

void ROVER_setSpeed(int speed1, int speed2) {
    MOTOR1_setSpeed(speed1);
    MOTOR2_setSpeed(speed2);
}

void ROVER_increaseSpeed(int acc) {
    MOTOR1_increaseSpeed(acc);
    MOTOR2_increaseSpeed(acc);
}

void ROVER_decreaseSpeed(int dec) {
    MOTOR1_decreaseSpeed(dec);
    MOTOR2_decreaseSpeed(dec);
}

void ROVER_stop() {
    MOTOR1_stop();
    MOTOR2_stop();
    ROVER_setMode(STOP_MODE);
}

void ROVER_setMode(int mode) {
    MODE = mode;
}