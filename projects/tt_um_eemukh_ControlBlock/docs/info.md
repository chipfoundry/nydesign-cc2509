<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project takes in the last 6-bits of a 32-bit wide instruction as the Opcode. The code passed in is from a 32-bit instruction from MIPS. The opcode is then passed through control logic which assigns the control signals to other components in a CPU. The signals are Register Destination, Branch, Memory Read, Memory to Register, ALU Opcode, Memory Write, ALU Source, and Register Write. The ALU OPcode is fed into the ALU control unit which also takes in as input the function bits (first 6-bits of 32-bit instruction) but only the first 4 bits. Then the ALU control Unit outputs the 4 operational code instructions to be fed into an ALU for a CPU. Bits 4 and 5 of the funct. input are set as 0 and 1 , respectively, as default given this chip is designed to  work for a limited number of MIPS32 instrucions.

## How to test

The project can be used to test certain instructions be R-type instructions (add, subtract, AND, OR, Set on Less Then), Store Word, Load Word, and Branch instructions. You would input your MIPS into a CPU as this chip will be connected with other components in the CPU such as the Program Counter, the ALU, the registers, and the Instruction Memory Unit (Instruction Register). You can probe the physical chip to see if the outputs match the functional code and ALU Operational code for those specfic instructions.

## External hardware

Decoder to separate the bits for the code inputs. Registers for writing, reading, inputting MIPS32 instructions. 
