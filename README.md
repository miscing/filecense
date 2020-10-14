# Filecense

Simple python script that recusively walks directory and adds license header at top and full text into a seperate file. See '-h' for usage information

You can use the docker image in ci/cd, just pass the license holder name as 'Joseph Connor' when you run it, it will automatically attempt to add the license to the directory of the current project.

## NOTES:
 - `license_holder` argument must come before options with multiple values

### USAGE:

```
usage: filecense [-h] [-d DATE] [-l LICENSE] [-list] [-ln LICENSE_FILE_NAME]
                 [-sd SKIPDIR [SKIPDIR ...]] [-sf SKIPFILE [SKIPFILE ...]] [-re] [-p PATH]
                 [-f FORMAT] [-c COMMENT] [-v]
                 license_holder

positional arguments:
  license_holder        name of licence holder, use quotation marks to include whitespace

optional arguments:
  -h, --help            show this help message and exit
  -d DATE, --date DATE  year to use, no sanity checks will be used literally
  -l LICENSE, --license LICENSE
                        specifies license to add
  -list, --listlicenses
                        lists available licenses
  -ln LICENSE_FILE_NAME, --license_file_name LICENSE_FILE_NAME
                        specifies name of license file, default LICENSE
  -sd SKIPDIR [SKIPDIR ...], --skipdir SKIPDIR [SKIPDIR ...]
                        sets directories to skip
  -sf SKIPFILE [SKIPFILE ...], --skipfile SKIPFILE [SKIPFILE ...]
                        sets files to skip
  -re, --regex          together with skip flags causes arguments to be interpreted as regex
                        strings
  -p PATH, --path PATH  specifies path to parse, default is current directory
  -f FORMAT, --format FORMAT
                        specifies comment syntax based on language, such as py for python
                        comments. Usually unnecessary
  -c COMMENT, --comment COMMENT
                        places provided string at the front of every sentence of top
                        template, overrides format option
  -v, --verbose         increased verbosity
```

