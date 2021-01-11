# Filecense

Simple python program that recursively walks directory and adds license header at top and full text into a separate file. See '-h' for usage information

Docker image at: `registry.gitlab.com/miscing/filecense/filecense`
You can use the docker image for ci/cd, just pass the license holder name as 'Joseph Connor' when you run it, it will automatically attempt to add the license to the directory of the current project. The syntax is thus `docker/podman run registry.gitlab.com/miscing/filecense/filecense "Joseph Connor" [options]`

## Features:
 - License detection, will attempt to detect if file has a license and skip it. Detection is extremely rudimentary and meant for adding license to new files, so all arguments must be identical (including date), meant for use in CICD with heavy flag usage
 - Automatic source code language detection (by extension), and correct commenting
 - Ignores files that should not have a license, and you can use flags to add ignorables.

## Notes:
 - Remaining arguments are license holder
 - Some flags allow multiple items, make sure there is some flag between them and license holder (flag `-e` is provided for this that does nothing)

### USAGE:

```
usage: filecense.py [-h] [-p PATH] [-d DATE] [-l LICENSE] [-f] [-list]
                    [-ln LICENSE_FILE_NAME] [-e] [-sd SKIPDIR [SKIPDIR ...]]
                    [-sf SKIPFILE [SKIPFILE ...]] [-re] [-fmt FORMAT [FORMAT ...]]
                    [-c COMMENT] [-v]
                    ...

positional arguments:
  license_holder        Name of licence holder.use quotation marks to include whitespace.
                        Place as first argument for safe usage with other flags. Default
                        license: EUPL

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Specifies path to parse, defaults to current directory
  -d DATE, --date DATE  Date to use, used as provided
  -l LICENSE, --license LICENSE
                        Specifies license to add
  -f, --force           Overrides checks and user input.
  -list, --listlicenses
                        Lists available licenses
  -ln LICENSE_FILE_NAME, --license_file_name LICENSE_FILE_NAME
                        Specifies name of license file, default LICENSE
  -e, --end             Does nothing, use to end a multi item flag before providing license
                        holder
  -sd SKIPDIR [SKIPDIR ...], --skipdir SKIPDIR [SKIPDIR ...]
                        Sets directories to skip. Make sure you have a flag before license
                        holder
  -sf SKIPFILE [SKIPFILE ...], --skipfile SKIPFILE [SKIPFILE ...]
                        Sets files to skip. Make sure you have a flag before license holder
  -re, --regex          Use with skip flags, causes arguments to be interpreted as regex
                        strings
  -fmt FORMAT [FORMAT ...], --format FORMAT [FORMAT ...]
                        Add filetype comment syntax. EXT/REGEX=SYNTAX. Make sure you have a
                        flag before license holder. Example: '-f .ext=!! Dockerfile=#' Use
                        '.ext' for extension detection, otherwise will be interpreted as a
                        regex string
  -c COMMENT, --comment COMMENT
                        Set comment syntax, replaces filetype detection
  -v, --verbose         Increased verbosity
```
