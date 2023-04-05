//
// Created by Leon Kabue on 3/25/23.
//

#ifndef FINAL_MOTOR_H
#define FINAL_MOTOR_H

#include "avr/io.h"

#define DIR PORTB
#define BRAKE PORTB

#define LEFT_SPEED OCR2B
#define LEFT_DIR PORTB4
#define LEFT_BRAKE PORTB1

#define RIGHT_SPEED OCR2A
#define RIGHT_DIR PORTB5
#define RIGHT_BRAKE PORTB0


void TIMER_SETUP();

void LEFT_init();
void RIGHT_init();

void LEFT_forward(int speed);
void RIGHT_forward(int speed);

void LEFT_backward(int speed);
void RIGHT_backward(int speed);

void LEFT_setSpeed(int speed);
void RIGHT_setSpeed(int speed);

void LEFT_increaseSpeed(int acc);
void RIGHT_increaseSpeed(int acc);

void LEFT_decreaseSpeed(int dec);
void RIGHT_decreaseSpeed(int dec);

void LEFT_stop();
void RIGHT_stop();

#endif //FINAL_MOTOR_H
