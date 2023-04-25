//
// Created by Leon Kabue on 4/20/23.
//

#include "distance.h"


void DISTANCE_init() {
	//clear power reduction for ADC
	PRR &= ~(1<<PRADC);

	//select Vref = AVcc
	ADMUX |= (1<<REFS0);
	ADMUX &= ~(1<<REFS1);

	//set ADC prescalar to 128 (125 kHz)
	ADCSRA |= (1<<ADPS0);
	ADCSRA |= (1<<ADPS1);
	ADCSRA |= (1<<ADPS2);

	//Enable ADC
	ADCSRA |= (1<<ADEN);
}

uint16_t DISTANCE1_read() {
	//set ADC channel as pin A2
	ADMUX &= ~(1<<MUX0);
	ADMUX |= (1<<MUX1);
	ADMUX &= ~(1<<MUX2);
	ADMUX &= ~(1<<MUX3);

	//disable digital input buffer on ADC pin
	DIDR0 |= (1<<ADC0D);

	//start conversion
	ADCSRA |= (1<<ADSC);

	//wait for conversion to complete
	while (ADCSRA&(1<<ADSC));

	return ADC;
}
uint16_t DISTANCE2_read() {
	//set ADC channel as pin A3
	ADMUX |= (1<<MUX0);
	ADMUX |= (1<<MUX1);
	ADMUX &= ~(1<<MUX2);
	ADMUX &= ~(1<<MUX3);

	//disable digital input buffer on ADC pin
	DIDR0 |= (1<<ADC0D);

	//start conversion
	ADCSRA |= (1<<ADSC);

	//wait for conversion to complete
	while (ADCSRA&(1<<ADSC));

	return ADC;
}

float getDistance1() {
	uint16_t distance = DISTANCE1_read();

	if (distance <= 512) {
		if (distance >= 409) {
			return 100.f + ((512 - (float) distance) / (512 - 409) * 50);
			} else {
			if (distance >= 369) {
				return 150.f + ((409 - (float) distance) / (409 - 369) * 50);
				} else {
				if (distance >= 338) {
					return 200.f + ((369 - (float) distance) / (369 - 338) * 50);
					} else {
					if (distance >= 317) {
						return 250.f + ((338 - (float) distance) / (338 - 317) * 50);
						} else {
						if (distance >= 307) {
							return 300.f + ((317 - (float) distance) / (317 - 307) * 50);
							} else {
							if (distance >= 297) {
								return 350.f + ((307 - (float) distance) / (307 - 297) * 50);
								} else {
								if (distance >= 287) {
									return 400.f + ((297- (float) distance) / (297 - 287) * 50);
									} else {
									if (distance >= 277) {
										return 450.f + ((287 - (float) distance) / (287 - 277) * 50);
										} else {
										return 500.f;
									}
								}
							}
						}
					}
				}
			}
		}
	}
	return 99;
}

float getDistance2() {
	uint16_t distance = DISTANCE2_read();

	if (distance <= 461) {
		if (distance >= 266) {
			return 10 + ((461 - (float)distance) / (461 - 266) * 10);
			} else {
			if (distance >= 184) {
				return 20 + ((266 - (float)distance) / (266 - 184) * 10);
				} else {
				if (distance >= 154) {
					return 30 + ((184 - (float)distance) / (184 - 154) * 10);
					}  else {
					if (distance >= 123) {
						return 40 + ((154 - (float)distance) / (154 - 123) * 10);
						} else {
						if (distance >= 102) {
							return 50 + ((123 - (float)distance) / (123 - 102) * 10);
							} else  {
							if (distance >= 92) {
								return 60 + ((102 - (float)distance) / (102 - 92) * 10);
								} else {
								if (distance >= 82) {
									return 70 + ((92 - (float)distance) / (92 - 82) * 10);
									} else {
									return 80;
								}
							}
						}
					}
				}
			}
		}
	}
	return 5;
}