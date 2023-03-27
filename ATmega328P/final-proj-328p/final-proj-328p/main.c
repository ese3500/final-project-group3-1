#define F_CPU 16000000UL
#define BAUD_RATE 9600
#define BAUD_PRESCALER (((F_CPU / (BAUD_RATE * 16UL))) - 1)

#include <avr/interrupt.h>
#include <util/delay.h>

#include "tests/roverTests.h"
#include "tests/serialTests.h"


void Initialize() {
    cli();
    //ROVER_initialize();
    sei();
}

int main(void) {
    Initialize();

    _delay_ms(1000);
    //testRover();
    //echoSerial();
	twoWaySerialTest();

    while(1);
}

