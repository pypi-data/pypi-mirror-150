# Seqits

 Seqits provides several useful toosl for sequences processing. 

## Installation method

`pip install seqits `

## Tools

#### Seqits

`python -m seqits -v # display the version of Seqits`  
`python -m seqits list # display all tools in Seqits`  

#### randseq

This tool can generate cds or protein sequence(s) randamly.

| Arguments      | Description                                                    |
| -------------- |:--------------------------------------------------------------:|
| type           | nucl/prot, cds or protein sequence(s)                          |
| num            | number of sequences(s) to generate                             |
| out (optional) | output file, defaut: output.fa                                 |
| show(optional) | whether display the output on the screen or not, defaut: false |

e.g.   
`python -m seqits.randseq nucl 100 -o output.fa -s true`

#### search

This tool can search and extract  sequence(s) you want by  Gene ID or Gene Name.

| Arguments       | Description                                                                                                                                                        |
| --------------- |:------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| input           | input raw fasta file                                                                                                                                               |
| gene            | input gene(s)                                                                                                                                                      |
| type (optional) | re/string/file, type of input gene(s). re means regulate expression, for file, one gene one line; for string, gene(s) should be seperated with ',', default string |
| mode (optional) | fast/order, "fast" mode may faster than "order" mode, but "order" mode can display your output accoring to the order of input gene(s), default: fast               |
| out (optional)  | output file, defaut: output.fa                                                                                                                                     |
| show (optional) | whether display output on the screen or not, defaut: false                                                                                                         |

e.g.   
`python -m seqits.search input.fa Gene1,Gene2,Gene3 --out output.fa`  
`python -m seqits.search input.fa Gene.txt -t file`  

#### formatseq

This tool can format the fasta file.

| Arguments       | Description                                                |
| --------------- |:----------------------------------------------------------:|
| input           | input raw fasta file                                       |
| num (optional)  | number of characters per line, defaut: 60                  |
| out (optional)  | output file, defaut: output.fa                             |
| show (optional) | whether display output on the screen or not, defaut: false |

e.g.   
`python -m seqits.formatseq input.fa 100`  

#### retest

This tool can test the regulate expression.

| Arguments | Description         |
| --------- |:-------------------:|
| input     | input file          |
| re        | regulate expression |

e.g.   
`python -m seqits.retest input.fa ">(Gene\d{1,3})"`  
