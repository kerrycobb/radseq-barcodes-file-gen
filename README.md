# Usage
Replace values in the sample_id column of the `template.csv` file. File
can contain other data as well. It must at least have the columns found
in the `template.csv` file.

Requires the packages `fire` and `pandas`.

Run:
```bash
./generate_barcodes.py <csv file> <read1 enzyme> <read2 enzyme> 
```
Script outputs a single csv file called `out.csv` that contains the bar code sequences 
as well as other data from the input file.

It also outputs a tab delimited barcodes file for each plate which can be used with Stacks or ipyrad

The i7-indexes.tsv file contains the i7 index sequences. This file can be edited for demultiplexing i7 indexes.

# Notes
Read 1 corresponds to i7 end of read
Read 2 corresponds to i5 end of read

The naming of the read 1 enzyme is confusing as the enzymes are named for 
the enzyme doing the adapter dimer cutting rather than the enzyme cutting the 
DNA. If not using the third adapter dimer cutting enzyme, the name of 
the read 1 enzyme will not correspond with the enzyme that you used. 
