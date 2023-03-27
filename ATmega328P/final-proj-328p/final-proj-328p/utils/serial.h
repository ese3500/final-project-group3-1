/*
 * serial.h
 *
 * Created: 2/17/2023 11:02:57
 *  Author: Kenzo
 */ 
#ifndef SERIAL_H
#define SERIAL_H

void SerialInit(int prescaler);

void SerialPrintChar(unsigned char data);

void SerialPrint(char* StringPtr);

void SerialReadLine(char *out);

#endif