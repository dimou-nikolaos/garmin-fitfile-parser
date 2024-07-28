[![Pylint](https://github.com/dimou-nikolaos/garmin-fitfile-parser/actions/workflows/pylint.yml/badge.svg?event=push)](https://github.com/dimou-nikolaos/garmin-fitfile-parser/actions/workflows/pylint.yml)
# garmin-fitfile-parser

Parser for Garmin's fitfiles

## Installation

- Install python3.10-venv if you don't have it already:
```
sudo apt install python3.10-venv
```

- Create and activate virtual environment:
```
python3 -m venv env
source env\bin\activate
```

- Install requirements:
```
pip install -r requirements.txt
```

## How to download fitfile for a garmin activity
- Login to account
- Open activity
- Click the cogwheel in the upper right corner
- Click Export File
- Unzip fitfile

## How to dump Activity's segments:
Run:
```
python3 fitfile_segments_parser.py <path_to_fitfile>
```


## How to plot Activity's pace:
Run:
```
python3 fitfile_pace_plotter.py <path_to_fitfile>
```

## How to deactivate virtual environment
Run:
```
deactivate
```
