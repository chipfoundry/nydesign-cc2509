<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works
This alu was designed to do addition subtration bitwise and and bitwise or based on the two four bit binary numbers input by the user. It does all of these at the same time and the output is selected using a multiplexer. The inputs are grouped in bitwise pairs a with b c with d ect. The resulting numbers are "geca" and "hfdb" where a and b are the least signifigant bits in subtraction "hfdb" is subtracted from "geca". The two selector bits s1 and s2 decide the function. (00=bwand, 10=bwor, 01=addition,  11=subtraction)
Explain how your project works

## How to test
testing can be conducted by selecting an operation picing two input numbers and comparing the output to hand by calcultions
Explain how to use your project

## External hardware
Connect the 5 outputs to leds to see the resultant number
List external hardware used in your project (e.g. PMOD, LED display, etc), if any
