# ExecParser

[![PyPI version](https://badge.fury.io/py/ExecParser.svg)](https://badge.fury.io/py/ExecParser)
![GitHub](https://img.shields.io/github/license/r33-L1/ExecParser)

Parse PE, ELF, and Mach-O using lief

# Installation
Simply run 
```
pip install ExecParser
```
# Usage
```
usage: python3 Execparser [-h] [-v] [--version] [--header] [-seg] [-sec] [-segi SEGMENT_INFO] [-seci SECTION_INFO] [EXECUTABLE]

Executable files analyzing and modification

positional arguments:
  EXECUTABLE            Executable file to parse

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Set verbosity level
  --version             Print current version of ExecParser
  --header              Print header
  -seg, --segments      Print sections
  -sec, --sections      Print segments
  -segi SEGMENT_INFO, --segment_info SEGMENT_INFO
                        Print additional segment info
  -seci SECTION_INFO, --section_info SECTION_INFO
                        Print additional section info
                        
```

# Development roadmap

### v0.4
 - PE parse 
 - Strings view & search
 - Imported & Exported functions view

### v0.6
 
 - Basic security checks for PE, Mach-O, ELF
 - Further analysis of specific addresses

### v1.0

 - Modify binaries

### v2.0 

 - Create binaries from scratch
