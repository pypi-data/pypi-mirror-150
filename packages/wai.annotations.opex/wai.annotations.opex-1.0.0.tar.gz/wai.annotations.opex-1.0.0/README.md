# wai-annotations-opex
wai.annotations module for managing datasets with [OPEX](https://github.com/WaikatoLink2020/objdet-predictions-exchange-format) annotations. 

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

## Plugins
### FROM-OPEX-OD
Reads image object-detection annotations in the OPEX format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: from-opex-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME] [--seed SEED]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into
  --seed SEED           the seed to use for randomisation
```

### TO-OPEX-OD
Writes image object-detection annotations in the OPEX format

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
usage: to-opex-od [-c PATH] [-l PATH] [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  -c PATH, --labels-csv PATH
                        Path to the labels CSV file to write
  -l PATH, --labels PATH
                        Path to the labels file to write
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        output directory to write images and annotations to
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```
