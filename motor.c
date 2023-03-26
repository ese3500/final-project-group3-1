//
// Created by Leon Kabue on 3/25/23.
//

#include "motor.h"

/*We will be using timer1 to control both motors via a PWM signal on pins PB1(OC1A) and PB2(0C1B)*/
void TIMER1_SETUP() {
    //set up timer1 with no pre-scaling
    TCCR1B |= (1<<CS10);

    //setting timer1 to phase correct PWM
    TCCR1A |= (1<<WGM10);

    //setting OC1A and OC1B to non-inverting mode (clear on compare match)
    TCCR1A |= (1<<COM1A1);
    TCCR1A |= (1<<COM1B1);
}

void MOTOR1_init() {

    //MOTOR1 enable pin attached to pin PB1(OC1A)
    //MOTOR1 direction pin is attached to pin PBO
    //MOTOR1 brake pin is attached to pin PD7

    //setting PB1, PB0,and PD7 as output pins
    DDRB |= (1<<DDB1);
    DDRB |= (1<<DDB0);
    DDRD |= (1<<DDD7);

    MOTOR1_setSpeed(0);
}

void MOTOR2_init() {
    //MOTOR2 enable pin attached to pin PB2(OC1B)
    //MOTOR2 direction pin is attached to pin PD6
    //MOTOR2 brake pin is attached to pin PD5

    //setting PB2, PD6,and PD5 as output pins
    DDRB |= (1<<DDB2);
    DDRD |= (1<<DDD6);
    DDRD |= (1<<DDD5);

    MOTOR2_setSpeed(0);
}

void MOTOR1_forward() {
    //set direction pin to high and brake pin to low
    PORTB |= (1<<PORTB0);
    PORTD &= ~(1<<PORTD7);
}

void MOTOR2_forward() {
    //set direction pin to high and brake pin to low
    PORTD |= (1<<PORTD6);
    PORTD &= ~(1<<PORTD5);
}

void MOTOR1_backward() {
    //set direction pin to low and brake pin to low
    PORTB &= ~(1<<PORTB0);
    PORTD &= ~(1<<PORTD7);
}

void MOTOR2_backward() {
    //set direction pin to low and brake pin to low
    PORTD &= ~(1<<PORTD6);
    PORTD &= ~(1<<PORTD5);
}

//speed value should be between 0 and 255
void MOTOR1_setSpeed(int speed) {
    if (speed > 255) {
        MOTOR1_SPEED = 255;
    } else {
        if (speed < 0) {
            MOTOR1_SPEED = 0;
        } else {
            MOTOR1_SPEED = speed;
        }
    }
}

//speed value should be between 0 and 255
void MOTOR2_setSpeed(int speed) {
    if (speed > 255) {
        MOTOR2_SPEED = 255;
    } else {
        if (speed < 0) {
            MOTOR2_SPEED = 0;
        } else {
            MOTOR2_SPEED = speed;
        }
    }
}

void MOTOR1_increaseSpeed(int acc) {
    if (acc < 255 && MOTOR1_SPEED <= 255-acc) {
        MOTOR1_SPEED += acc;
    }
}

void MOTOR2_increaseSpeed(int acc) {
    if (acc < 255 && MOTOR2_SPEED <= 255-acc) {
        MOTOR2_SPEED += acc;
    }
}

void MOTOR1_decreaseSpeed(int dec) {
    if (MOTOR1_SPEED >= dec) {
        MOTOR1_SPEED -= dec;
    }
}

void MOTOR2_decreaseSpeed(int dec) {
    if (MOTOR2_SPEED >= dec) {
        MOTOR2_SPEED -= dec;
    }
}

void MOTOR1_stop() {
    //set the brake pin to high
    PORTD |= (1<<PORTD7);
}

void MOTOR2_stop() {
    //set the brake pin to high
    PORTD |= (1<<PORTD5);
}