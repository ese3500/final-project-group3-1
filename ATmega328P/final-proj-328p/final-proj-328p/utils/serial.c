/*
 * serial.c
 *
 * Created: 2/17/2023 11:02:18
 *  Author: Kenzo
 */ 
/*
 * lab3 part a.c
 *
 * Created: 2/17/2023 10:53:06
 * Author : Kenzo
 */ 


#include <avr/io.h>
#include "serial.h"

void SerialInit(int prescaler)
{
	
	/*Set baud rate */
	UBRR0H = (unsigned char)(prescaler>>8);
	UBRR0L = (unsigned char)prescaler;
	//Enable receiver and transmitter
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	/* Set frame format: 2 stop bits, 8 data bits */
	UCSR0C = (1<<UCSZ01) | (1<<UCSZ00); // 8 data bits
	UCSR0C |= (1<<USBS0); // 2 stop bits
}

void SerialPrintChar(unsigned char data)
{
	// Wait for empty transmit buffer
	while(!(UCSR0A & (1<<UDRE0)));
	// Put data into buffer and send data
	UDR0 = data;
	
}

void SerialPrint(char* StringPtr)
{
	while(*StringPtr != 0x00)
	{
		SerialPrintChar(*StringPtr);
		StringPtr++;
	}
}

void SerialReadLine(char *out) {
    int index = 0;
    char cur_char = '\0';

	while (cur_char != '\r' && cur_char != '\n') {
		while(!(UCSR0A & (1 << RXC0)));

		cur_char = (char) UDR0;
		out[index++] = cur_char;
	}

	out[index] = '\0';
}
