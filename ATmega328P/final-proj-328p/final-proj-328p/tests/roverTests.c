#include "roverTests.h"
#include "../utils/rover.h"

#define F_CPU 16000000UL
#define BAUD_RATE 9600
#define BAUD_PRESCALER (((F_CPU / (BAUD_RATE * 16UL))) - 1)

#include <util/delay.h>

void testRover() {

    //move forward for 5 seconds with constant speed
    ROVER_start(255);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //move backward for 5 seconds with constant speed
    ROVER_moveBackward(255);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //move to the left for 5 seconds with constant speed
    ROVER_turnLeft(255);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //move to the right for 5 seconds with constant speed
    ROVER_turnRight(255);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //turn around for 5 seconds with constant speed
    ROVER_turnAround(255);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //move forward with increasing speed then decreasing speed then stop
    ROVER_moveForward(50);
    for (int sp = 50; sp <=255; sp++) {
        ROVER_setSpeed(sp, sp);
        _delay_ms(20);
    }
    for (int sp = 255; sp >= 0; sp--) {
        ROVER_setSpeed(sp, sp);
        _delay_ms(20);
    }
    ROVER_stop();
    _delay_ms(100);

    //move backward with increasing speed then decreasing speed then stop
    ROVER_moveBackward(50);
    for (int sp = 50; sp <=255; sp++) {
        ROVER_setSpeed(sp, sp);
        _delay_ms(20);
    }
    ROVER_stop();
    _delay_ms(100);
    for (int sp = 255; sp >= 0; sp--) {
        ROVER_setSpeed(sp, sp);
        _delay_ms(20);
    }

    //move forward for 5 seconds with constant speed
    ROVER_start(100);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //move backward for 5 seconds with constant speed
    ROVER_moveBackward(100);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //move to the left for 5 seconds with constant speed
    ROVER_turnLeft(100);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //move to the right for 5 seconds with constant speed
    ROVER_turnRight(100);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //turn around for 5 seconds with constant speed
    ROVER_turnAround(100);
    _delay_ms(5000);
    ROVER_stop();
    _delay_ms(100);

    //move forward with increasing speed then decreasing speed then stop
    ROVER_moveForward(50);
    for (int sp = 50; sp <=255; sp++) {
        ROVER_setSpeed(sp, sp);
        _delay_ms(20);
    }
    for (int sp = 255; sp >= 0; sp--) {
        ROVER_setSpeed(sp, sp);
        _delay_ms(20);
    }
    ROVER_stop();
    _delay_ms(100);

    //move backward with increasing speed then decreasing speed then stop
    ROVER_moveBackward(50);
    for (int sp = 50; sp <=255; sp++) {
        ROVER_setSpeed(sp, sp);
        _delay_ms(20);
    }
    ROVER_stop();
    _delay_ms(100);
    for (int sp = 255; sp >= 0; sp--) {
        ROVER_setSpeed(sp, sp);
        _delay_ms(20);
    }

}