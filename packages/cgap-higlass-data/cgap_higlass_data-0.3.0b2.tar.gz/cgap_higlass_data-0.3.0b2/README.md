
# higlass-data
Package that creates data files for CGAP's Higlass browsers

## Installation

Simply run `pip install cgap-higlass-data` to install the package. You need at least Python 3.8.

To develop this package, clone this repo, make sure `poetry` is installed on your system and run `make install`.

## Commands

After installation the following commands can be run from the command line:

### Convert BED file to BW (bigWig) file

Assume you have a BED file of the form
```
# HEADER LINE 1
# HEADER LINE 2
chr1	0	1024	.	423
chr1	1024	2048	.	32
chr1	2048	3072	.	734
```
This BED file can be converted to a BW file with the following command

```
# -i input BED file path
# -o output BW file path
# -a assembly (currently only 'hg38' is supported
# -l number of header lines in the BED file
convert-bed-to-bw -i ./PATH/input.bed \
                  -o ./PATH/output.bw \
                  -a hg38 \
                  -l 2

```
Note that the `bedGraphToBigWig` must be installed on your system for this to work. It can be installed via conda (`conda install -c bioconda ucsc-bedgraphtobigwig`). You can also download the binary here: http://hgdownload.soe.ucsc.edu/admin/exe/

### Create variant-level VCF for CGAP's cohort browser

This command creates a multiresolution VCF file that is compatible to CGAP's cohort browser. Typically, the input VCF will be VEP annotated and has at least the info field `level_most_severe_consequence` (which is one of `HIGH`, `LOW`, `MODERATE`, `MODIFIER`) and an importance value that can ranks/sorts the variants. The info field that is used for that purpose can be set dynamically.

```
# -i input VCF path
# -o output VCF path
# -c info field in the input VCF that ranks the variants
# -m maximal tile values per consequence. Controls how may variants are displayed at once and a certain zoom level
# -q quiet True / False. Toggles verbose output
create-cohort-vcf -i ./PATH/input.vcf \
                  -o ./PATH/output.vcf \
                  -c p_value_negative_log_10 \
                  -q True

```

### Create coverage BED file from VCF

Counts the number of variants in a 1024bp window and creates a BED file with the results.

```
# -i input VCF path
# -o output VCF path
# -a assembly
# -q quiet True / False. Toggles verbose output
create-coverage-bed -i ./PATH/input.vcf \
                    -o ./PATH/output.bed \
                    -a hg38 \
                    -q True

```

