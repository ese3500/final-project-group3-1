#ifndef F_CPU
#define F_CPU 16000000UL
#define BAUD_RATE 9600
#define BAUD_PRESCALER (((F_CPU / (BAUD_RATE * 16UL))) - 1)
#endif

#include "serialTests.h"
#include "../utils/serial.h"

void echoSerial() {
    SerialInit(BAUD_PRESCALER);
    SerialPrint("Initialized!\n");
    char buf[100];

    while (1) {
        SerialPrint("Reading line...\n");
        SerialReadLine(buf);
        SerialPrint(buf);
    }
}