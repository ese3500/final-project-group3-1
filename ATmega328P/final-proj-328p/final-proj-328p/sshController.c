#ifndef F_CPU
#define F_CPU 16000000UL
#define BAUD_RATE 9600
#define BAUD_PRESCALER (((F_CPU / (BAUD_RATE * 16UL))) - 1)
#endif

#define __DELAY_BACKWARD_COMPATIBLE__

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "util/delay.h"
#include "utils/rover.h"
#include "utils/serial.h"
#include "utils/others.h"

#define DEFAULT_SPEED 180

char buf[100];

int get_arg(char *cmd, int start_index, int size) {
    char buf2[40];
    strcpy(buf2, cmd);
    buf2[start_index + size] = '\0';
    return atoi(cmd + start_index);
}

void command_responder(char *command) {
    if (!strncmp(command, "SPEED", 5)) {
        ROVER_setSpeed(get_arg(command, 6, 3), get_arg(command, 10, 3));
        _delay_ms(get_arg(command, 14, 7));
    } else if (!strncmp(command, "MOVE", 4)) {
        if (command[5] == 'F') ROVER_moveForward(DEFAULT_SPEED);
        else if (command[5] == 'B') ROVER_moveBackward(DEFAULT_SPEED);
        else if (command[5] == 'R') {
			ROVER_turnRight(DEFAULT_SPEED);
			_delay_ms(500);
			ROVER_stop();
		}
        else if (command[5] == 'L') {
			ROVER_turnLeft(DEFAULT_SPEED);
			_delay_ms(500);
			ROVER_stop();
		}
        else if (command[5] == 'U') {
            ROVER_turnAround(DEFAULT_SPEED);
            _delay_ms(500);
            ROVER_stop();
            }
        else if (command[5] == 'S') ROVER_stop();
    } else if (!strncmp(command, "DIST", 4)) {
        sprintf(buf, "%d\n", getDist());
		SerialPrint(buf);
    }
}

int main() {
    SerialInit(BAUD_PRESCALER);
    ROVER_initialize();
    DISTANCE_init();

    while (1) {
        SerialReadLine(buf);
        command_responder(buf);
    }

    return 0;
}

