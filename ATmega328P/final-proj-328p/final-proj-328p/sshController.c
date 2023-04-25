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
#include "utils/distance.h"

#define DEFAULT_SPEED 180

static int speed_left = DEFAULT_SPEED;
static int speed_right = DEFAULT_SPEED;

static char buf[100];
static char ack[4] = {'A', 'C', 'K', '\0'};
 
int get_arg(char *cmd, int start_index, int size) {
    char buf2[40];
    strcpy(buf2, cmd);
    buf2[start_index + size] = '\0';
    return atoi(cmd + start_index);
}

void command_responder(char *command) {
    if (!strncmp(command, "SPEED", 5)) {
        // ROVER_setSpeed(get_arg(command, 6, 3), get_arg(command, 10, 3));
        // _delay_ms(get_arg(command, 14, 7));
        speed_left = get_arg(command, 6, 3);
        speed_right = get_arg(command, 10, 3);
        SerialPrint(ack);
    } else if (!strncmp(command, "MOVE", 4)) {
        if (command[5] == 'F') {
            ROVER_moveForward2(speed_left, speed_right);
        } else if (command[5] == 'B') {
            ROVER_moveBackward2(speed_left, speed_right);
        } else if (command[5] == 'R') {
			ROVER_turnRight(speed_right);
		}
        else if (command[5] == 'L') {
			ROVER_turnLeft(speed_left);
		}
        else if (command[5] == 'U') {
            ROVER_turnAround2(speed_left, speed_right);
        }
        else if (command[5] == 'S') {
            ROVER_stop();
        }
        SerialPrint(ack);
    } else if (!strncmp(command, "DISTC", 5)) {
        sprintf(buf, "%d\n", getDistClose());
		SerialPrint(buf);
    } else if (!strncmp(command, "DISTF", 5)) {
        sprintf(buf, "%d\n", getDistFar());
        SerialPrint(buf);
    } else if (!strncmp(command, "DISTF", 5)) {
        sprintf(buf, "%d\n", getDistFar());
        SerialPrint(buf);
    } else if (!strncmp(command, "TEST", 4)) {
        SerialPrint("TEST");
    }
}

void align(int dist) {
    return;
}

int checkCollision() {
    if (getDistClose() < 20) {
        ROVER_stop();
        SerialPrint("COLLISION");
        align(30);
        
    }
}

int main() {
    SerialInit(BAUD_PRESCALER);
    ROVER_initialize();
    DISTANCE_init();

    while (1) {
        if (checkCollision()) {
            SerialPrint("DONE");
        }
        SerialReadLine(buf);
        command_responder(buf);
    }

    return 0;
}

