# CricketStats
A repository of Python code used to study ball-by-ball cricket data sourced from [cricsheet.org](cricsheet.org). The description of the Cricsheet yaml format can be found [here](https://cricsheet.org/format/yaml/#introduction-to-the-yaml-format).

## main.py
The file `main.py` uses the archive of men's Test matches and counts the occurrences of wickets, wides, and no-balls for each delivery in an over. It also displays the result of games, parsing the vairous options for results/ties/etc.

### Dependencies
Requires `ruamel.yaml` to parse yaml files from Cricsheet.