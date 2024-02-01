# scalar-network-analyzer

## Description
This project was created as my graduating project at the university.
Scalar network analyzer developed to measure frequency response of filters, amplifiers, transmission lines or other frequency-dependent circuits.

## About the project



## Demo video


## Block scheme 

The basic principle of operation of a scalar analyzer is to measure the amplitude of a transmission wave through a device under test (DUT). 
Such an analyzer contains both a signal source and a receiver. The source is used to obtain a known signal, while the receiver is used to 
determine changes in this signal caused by the circuit under test.

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/96fe6c5a-009a-445d-a68b-ca65a6429577)

The main component of the device is a signal generator SI5351 with 2 independent outputs, which has a square wave output signal, so it is 
impossible to use such a signal in a circuit with a broadband detector. So this was solved by using the architecture of a superheterodyne receiver.

The basic idea of a superheterodyne is a linear transfer of the spectrum to a specific frequency. This is achieved by synchronously changing the 
RF frequency (which is fed to the DUT) and the local oscillator (LO) frequency.

Next, the signal is filtered using piezoceramic filters at 455 kHz (this frequency was chosen because there are many cheap filters for this frequency) 
and amplified to use the full dynamic range of the logarithmic amplifier. After filtration, the signal will have a sinusoidal waveform.

The signal is fed to a logarithmic amplifier, the output of which is a constant voltage proportional to the power in dBm. The signal is then measured using an ADC
controller, processed with MCU and transmitted data to a computer via USB.



## Schematic

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/f8e9c527-c77a-45df-8c64-b73edbecdc98)

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/942bc0bf-1cdf-48b3-854c-eb4f2ee5fea3)

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/248fc41b-bde0-4913-9b84-5d0cf17100d0)

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/d2131c7b-b13a-4d74-b304-a5370287d571)

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/429baab3-91fa-4c22-894d-802e0431e550)


## Hardware
A 4-layer printed circuit board was designed and manufactured. I created two impedance profiles of 90 ohms for the USB interface and 50 ohms for high-frequency 
signal transmission lines, since the device must operate in systems with such wave impedance.

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/750847c2-5000-4ecb-8e42-d8fe2a1b10e1)

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/f5e0a811-b834-4143-be26-0406b90a589e)

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/a7b8261a-c680-41bd-9830-19379ac72967)

## Software
### CubeMX Connectivity 
![image](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/f87cdce6-87d8-4f01-a988-95ca98dc9529)

## PC Application

## Testing
The low-pass at 12 MHz LC filter was tested. The ideal characteristic in LTSpice is shown below.

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/c1b50dab-7780-4b7e-8cd6-7ac67b126c3d)

Measured characteristic with the use of the scalar analyzer is shown below. 

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/01a0b0be-3137-45f2-83df-2e151f7f25e4)

Also, an 8 MHz quartz resonator was measured.

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/653ef5a9-74e8-4fc6-8475-34848f43bcfa)

Below is a characteristic of a piezoceramic bandpass filter with unknown characteristics (similar to the one used in the device circuitry).
It should be added that the impedance of the filter (1500 ohms) is not matched to the device (50 ohms), which causes noticeable ripples in the passband.

![зображення](https://github.com/Ivanchenko59/scalar-network-analyzer/assets/80352225/9c534ed9-11de-42d1-b81d-4c4b9949949a)







