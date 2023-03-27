//
// Created by Leon Kabue on 3/25/23.
//

#ifndef FINAL_MOTOR_H
#define FINAL_MOTOR_H

#include "avr/io.h"

#define MOTOR1_SPEED OCR1A
#define MOTOR2_SPEED OCR1B

void TIMER1_SETUP();

void MOTOR1_init();

void MOTOR2_init();

void MOTOR1_forward();
void MOTOR2_forward();

void MOTOR1_backward();
void MOTOR2_backward();

void MOTOR1_setSpeed(int speed);
void MOTOR2_setSpeed(int speed);

void MOTOR1_increaseSpeed(int acc);
void MOTOR2_increaseSpeed(int acc);

void MOTOR1_decreaseSpeed(int dec);
void MOTOR2_decreaseSpeed(int dec);

void MOTOR1_stop();
void MOTOR2_stop();

#endif //FINAL_MOTOR_H
