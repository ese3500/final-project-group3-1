//
// Created by Leon Kabue on 5/4/23.
//

#include "LED.h"

void LED_initialize() {
    //setting pin PD5(PIN 5) for RED led output
    DDRD |= (1<<DDD5);

    //setting pin PD7(PIN 7) for RED led output
    DDRD |= (1<<DDD7);

    //setting pin PB2(PIN 10) for RED led output
    DDRB |= (1<<DDB2);
}

void LED_REDon() {
    PORTD |= (1<<PORTD5);
}

void LED_REDoff() {
    PORTD &= ~(1<<PORTD5);
}

void LED_BLUEon() {
    PORTD |= (1<<PORTD7);
}

void LED_BLUEoff() {
    PORTD &= ~(1<<PORTD7);
}

void LED_GREENon() {
    PORTB |= (1<<PORTB2);
}

void LED_GREENoff() {
    PORTB &= ~(1<<PORTB2);
}