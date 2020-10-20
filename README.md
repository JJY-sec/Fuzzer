# Fuzzer

## How to get coverage
### Use gcc feature
gcc -o file file.c --coverage
gcov file.c


## Class 
### Run
Run target program and save input that cause crash (sig6,sig11).


### Fuzzer
Calculate coverage.
Select high coverage input.
Generate Inputs.
