//
// Created by Leon Kabue on 5/4/23.
//

#include "LED.h"

void LED_initialize() {
    //setting pin PB0(PIN 8) for RED led output
    DDRB |= (1<<DDB0);

    //setting pin PB1(PIN 9) for RED led output
    DDRB |= (1<<DDB1);

    //setting pin PB2(PIN 10) for RED led output
    DDRB |= (1<<DDB2);
}

void LED_REDon() {
    PORTB |= (1<<PORTB0);
}

void LED_REDoff() {
    PORTB &= ~(1<<PORTB0);
}