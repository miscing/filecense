# Filecense

Simple python program that recursively walks directory and adds license header at top and full text into a separate file. See '-h' for usage information

Docker image at: `registry.gitlab.com/miscing/filecense/filecense`
You can use the docker image for ci/cd, just pass the license holder name as 'Joseph Connor' when you run it, it will automatically attempt to add the license to the directory of the current project. The syntax is thus `docker/podman run registry.gitlab.com/miscing/filecense/filecense "Joseph Connor" [options]`

## Features:
 - License detection, will attempt to detect if file has a license and skip it. Detection is extremely rudimentary and meant for adding license to new files, so all arguments must be identical (including date), meant for use in CICD with heavy flag usage
 - Automatic source code language detection (by extension), and correct commenting
 - Ignores files that should not have a license, and you can use flags to add ignorables.

## Notes:
 - Some flags allow multiple items, pass license holder as first argument when using them
 - Use quotes around whitespace in license holder

### USAGE:

```
usage: filecense.py [-h] [-d DATE] [-l LICENSE] [-list]
                    [-ln LICENSE_FILE_NAME] [-sd SKIPDIR [SKIPDIR ...]]
                    [-sf SKIPFILE [SKIPFILE ...]] [-re] [-p PATH]
                    [-fmt FORMAT [FORMAT ...]] [-c COMMENT] [-v]
                    license_holder

positional arguments:
  license_holder        Name of licence holder.use quotation marks to include
                        whitespace

optional arguments:
  -h, --help            show this help message and exit
  -d DATE, --date DATE  Year to use, no parsing
  -l LICENSE, --license LICENSE
                        Specifies license to add
  -list, --listlicenses
                        Lists available licenses
  -ln LICENSE_FILE_NAME, --license_file_name LICENSE_FILE_NAME
                        Specifies name of license file, default LICENSE
  -sd SKIPDIR [SKIPDIR ...], --skipdir SKIPDIR [SKIPDIR ...]
                        Sets directories to skip. Space seperate multiple
                        items
  -sf SKIPFILE [SKIPFILE ...], --skipfile SKIPFILE [SKIPFILE ...]
                        Sets files to skip. Space seperate multiple items
  -re, --regex          Use with skip flags, causes arguments to be
                        interpreted as regex strings
  -p PATH, --path PATH  Specifies path to parse defaults to current directory
  -fmt FORMAT [FORMAT ...], --format FORMAT [FORMAT ...]
                        Add filetype comment syntax. EXT/REGEX=SYNTAX. Space
                        seperate multiple items. Example: '-f .ext=!!
                        Dockerfile=#' Use '.ext' for extension detection,
                        otherwise will be interpreted as a regex string
  -c COMMENT, --comment COMMENT
                        Set comment syntax, replaces filetype detection
  -v, --verbose         Increased verbosity
```
