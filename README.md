![Version 1.0](https://img.shields.io/badge/version-v1.0-orange.svg)
![Python 3.9.2](https://img.shields.io/badge/python-3.9.2-blue.svg)
![Latest commit](https://img.shields.io/github/last-commit/kyletimmermans/hex2mips?color=darkgreen)
[![kyletimmermans Twitter](http://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Follow)](https://twitter.com/kyletimmermans)

# <div align="center">hex2mips</div>

*Coming in version 2.0*
<div>-If command line args, no "Yes/No" prompt, just show the conversion only, as instruction or hex code</div>
<div>-Add '-h' to show options, either command line args or normal mode</div>
<div>-Fix repo<div>
<div>&ensp;&ensp;-Update hex2mips.py and remove hex2mipsV2.py</div>
<div>&ensp;&ensp;-New output picture</div>
<div>&ensp;&ensp;-Instructions on how to use (-h)</div>
<div>&ensp;&ensp;&ensp;&ensp;https://www.tutorialspoint.com/python/python_command_line_arguments.htm</div>
<div>&ensp;&ensp;-Update local files (in 'cs' git clone)</div>
<div>&ensp;&ensp;-Update website picture</div>
<div>&ensp;&ensp;-Backups to mege.nz</div>

<div>&ensp;</div>

<div><ins><b>Can currently deal with the following instructions:</b></ins></div>
add, addu, sub, subu, and, or, nor, slt, sltu, sll, srl, mult, multu, div, divu, xor, jr, syscall, break, beq, bne, addi, addiu, andi, ori, slti, sltiu, lui, lw, sw, xori, lb, lbu, j, jal

<div>&ensp;</div>

<div><ins><b>Recognizes the current registers:</b></ins></div>
$zero, $at, $v0-$v1, $a0-$a3, $t0-$t7, $s0-$s7, $t8-$t9, $k0-$k1, $gp, $sp, $fp, $ra

### Sample Output:
<p align="center">
  <img src="https://github.com/kyletimmermans/hex2mips/blob/master/example_screenshot.png?raw=true" alt="Sample Output"/>
</p>

</br>

### Changelog
<div>v1.0: Initial-Relase</div>
<div>v2.0:</div>
<div>&ensp;&ensp;-Can now convert from MIPS instruction to hex</div>
<div>&ensp;&ensp;-Send hex or MIPS instruction through command line instead of getting text GUI</div>
<div>&ensp;&ensp;&ensp;&ensp;-See <em>hex2mips.py -h</em></div>
<div>&ensp;&ensp;-Better error handeling / messages and input sanitization</div>
<div>&ensp;&ensp;-General bug fixes</div>
<div>&ensp;&ensp;-More comments and diagram in header</div>
