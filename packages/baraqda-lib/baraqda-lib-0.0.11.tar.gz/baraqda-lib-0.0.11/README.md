# baraqda-lib
dev
Library to generate fake data reflects real data.

State: PoC

Library take counter(how much data should be generated) and language(specifies folder in which data should be written).
After invocation func `generate()`, data are reading to `_data` and `weights`. In next step the data is randomized
and added to variable `_draw`. This end the  process of randomization and return List of generated data.
We can also invocate function `stored_draw()` which returns data from last draw.

# How to run

After downloading folder, install libraries from requirements.txt
> pip install -r requirements.txt

Run examples to check if everything is correct.
> python3 example.py
> python3 example_addresses.py
> python3 example_person.py


# Generating data

Generating data take place in class `Generator()`. Instance of this class provide function to read data, store data,
display data that was read from files and most import make a toss.

## Functions in `Generator()`

`generator.draw(lang: str, data_type: str, count: int = 1, sep: str = ' ') -> List[str]`

Generate list of toss. This func isn't for normal use. Use `generator.generate()` instead.

`.generator.search_files(path, sep, lang) -> None:`

Search for files in folder `Data` and read them with func `generator.read_files()`. Running this function erase all stored data and read it again. Use with caution!

`generator.read_files(filepath, separator, lang, filename) -> None:`

Read files in desired path. You can use this function to read additional files but remember that names of files must be unique.

`generator.generate(lang: str, data_type: str, counter: int = 1, sep: str = ' ') -> List[str]`

Automation to search for files, read them and make a toss. This is default function that you should use. 

Example
> generator.generate('PL', 'female_first_name', 10, '\t')

Generating 10 polish, female first names. The `\t` point separator in files. 

Output


`generator.access_data(lang: str, data_type: str) -> Dict[str, list]`

Check if data is stored in class. If yes, returns this data. If no, print error message.

Example
> generator.access_data('PL', 'male_first_name')

OUTPUT
> 

## Generate polish person and address

To generate person and address we can use class Person and class Addresses 
This two class generate only fake polish person.

Library generate only person nat


