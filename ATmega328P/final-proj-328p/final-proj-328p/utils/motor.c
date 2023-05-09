//
// Created by Leon Kabue on 3/25/23.
//

#include "motor.h"

/*We will be using timer2 to control LEFT and RIGHT motor via PWM signals on pins PD3(OC2B) and PB3(0C2A) respectively*/
void TIMER_SETUP() {
    //set up timer2 with no pre-scaling
    TCCR2B |= (1<<CS20);

    //setting timer2 to phase correct PWM
    TCCR2A |= (1<<WGM20);

    //setting OC2A and OC2B to non-inverting mode (clear on compare match)
    TCCR2A |= (1<<COM2A1);
    TCCR2A |= (1<<COM2B1);

}
void LEFT_init() {
    //setting OCR2B to output on pin PD3(D3)
    DDRD |= (1<<DDD3);

    //setting direction pin to output on pin PB4(D12)
    DDRB |= (1<<DDB4);

    //setting brake pin to output on pin PB1(D9)
    DDRB |= (1<<DDB1);
}

void RIGHT_init() {
    //setting  OCR2A to output on pin PB3(D11)
    DDRB |= (1<<DDB3);

    //setting direction pin to output on pin PB5(D13)
    DDRB |= (1<<DDB5);

    //setting brake pin to output on pin PB0(D8)
    DDRB |= (1<<DDB0);
}

void LEFT_forward(int speed) {
    BRAKE &= ~(1<<LEFT_BRAKE);

    LEFT_setSpeed(speed);
    DIR |= (1<<LEFT_DIR);
}
void RIGHT_forward(int speed) {
    BRAKE &= ~(1<<RIGHT_BRAKE);

    RIGHT_setSpeed(speed);
    DIR &= ~(1<<RIGHT_DIR);

}

void LEFT_backward(int speed) {
    BRAKE &= ~(1<<LEFT_BRAKE);

    LEFT_setSpeed(speed);
    DIR &= ~(1<<LEFT_DIR);
}

void RIGHT_backward(int speed) {
    BRAKE &= ~(1<<RIGHT_BRAKE);

    RIGHT_setSpeed(speed);
    DIR |= (1<<RIGHT_DIR);

}

void LEFT_setSpeed(int speed) {
    if (speed <= 0) {
        LEFT_SPEED = 0;
    }
    if (speed > 0 && speed < 255) {
        LEFT_SPEED = speed;
    }
    if (speed >= 255) {
        LEFT_SPEED = speed;
    }
}
void RIGHT_setSpeed(int speed) {
    if (speed <= 0) {
        RIGHT_SPEED = 0;
    }
    if (speed > 0 && speed < 255) {
        RIGHT_SPEED = speed;
    }
    if (speed >= 255) {
        RIGHT_SPEED = speed;
    }
}

void LEFT_increaseSpeed(int acc) {
    if (LEFT_SPEED + acc >= 255) {
        LEFT_SPEED = 255;
    } else {
        LEFT_SPEED += acc;
    }
}
void RIGHT_increaseSpeed(int acc) {
    if (RIGHT_SPEED + acc >= 255) {
        RIGHT_SPEED = 255;
    } else {
        RIGHT_SPEED += acc;
    }
}

void LEFT_decreaseSpeed(int dec) {
    if (LEFT_SPEED - dec <= 0) {
        LEFT_SPEED = 0;
    } else {
        LEFT_SPEED -= dec;
    }
}
void RIGHT_decreaseSpeed(int dec) {
    if (RIGHT_SPEED - dec <= 0) {
        RIGHT_SPEED = 0;
    } else {
        RIGHT_SPEED -= dec;
    }
}

void LEFT_stop() {
    BRAKE |= (1<<LEFT_BRAKE);
}

void RIGHT_stop() {
    BRAKE |= (1<<RIGHT_BRAKE);
}
