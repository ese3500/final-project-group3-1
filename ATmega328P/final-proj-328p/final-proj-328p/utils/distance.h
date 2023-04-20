//
// Created by Leon Kabue on 4/20/23.
//

#include <avr/io.h>

#ifndef DISTANCE_H
#define DISTANCE_H

void DISTANCE_init();

uint16_t DISTANCE1_read();
uint16_t DISTANCE2_read();

float getDistance1();
float getDistance2();

#endif //DISTANCE_H
