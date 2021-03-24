![Version 2.0](https://img.shields.io/badge/version-v2.0-orange.svg)
![Python 3.9.2](https://img.shields.io/badge/python-3.9.2-blue.svg)
![Latest commit](https://img.shields.io/github/last-commit/kyletimmermans/hex2mips?color=darkgreen)
[![kyletimmermans Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/kyletimmermans)

# <div align="center">hex2mips</div>

Convert hex codes to MIPS instructions and vice versa, see <em>hex2mips.py -h</em> for more information

<div>&ensp;</div>

<div><ins><b>Can currently deal with the following instructions:</b></ins></div>
add, addu, sub, subu, and, or, nor, slt, sltu, sll, srl, mult, multu, div, divu, xor, jr, syscall, break, beq, bne, addi, addiu, andi, ori, slti, sltiu, lui, lw, sw, xori, lb, lbu, j, jal

<div>&ensp;</div>

<div><ins><b>Recognizes the current registers:</b></ins></div>
$zero, $at, $v0-$v1, $a0-$a3, $t0-$t7, $s0-$s7, $t8-$t9, $k0-$k1, $gp, $sp, $fp, $ra

### GUI Mode
<p align="center">
  <img src="https://github.com/kyletimmermans/hex2mips/blob/master/media/gui_1.png?raw=true" alt="GUI Mode"/>
</p>

### Command Line: Hex 2 MIPS
<p align="center">
  <img src="https://github.com/kyletimmermans/hex2mips/blob/master/media/command_line_h2m_1.png?raw=true" alt="Command Line Hex 2 MIPS"/>
</p>

### Command Line: MIPS 2 Hex
<p align="center">
  <img src="https://github.com/kyletimmermans/hex2mips/blob/master/media/command_line_m2h_1.png?raw=true" alt="Command Line MIPS 2 Hex"/>
</p>

### Usage / Help
<p align="center">
  <img src="https://github.com/kyletimmermans/hex2mips/blob/master/media/usage_help.png?raw=true" alt="Usage / Help"/>
</p>

</br>

### Changelog
<div>v1.0: Initial-Relase</div>
<div>v2.0:</div>
<div>&ensp;&ensp;-Can now convert from MIPS instruction to hex</div>
<div>&ensp;&ensp;-Send hex or MIPS instruction through command line instead of getting text GUI</div>
<div>&ensp;&ensp;&ensp;&ensp;-See <em>hex2mips.py -h</em></div>
<div>&ensp;&ensp;-Better error handeling / messages and input sanitization</div>
<div>&ensp;&ensp;-Hex letters outputted in uppercase letters</div>
<div>&ensp;&ensp;-General bug fixes</div>
<div>&ensp;&ensp;-More comments and diagram in header</div>
