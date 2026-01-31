# Project Title

GmE 205 Lab Exercise 1

## Description

Codebase for GmE 205 Lab Exercise 1

## Getting Started

### Dependencies

* pandas
* matplotlib

### Installing

* Install the requirements
```pip install -r requirements.txt```

### Executing program

* Create a python virtual environment 
```py -m venv .venv```
* Activate the environment
```.\.venv\Scripts\activate```

## Reflection

* Abstraction: What did you choose to inspect, and why?
- I inspected a points.csv file that contains point data with latitude and longitude columns.

* Representation: What assumptions are you making about the CSV and coordinates?
- It is assumed that the csv file has a lat and lon column

* Responsibility: What should the script check automatically vs what a human should check?
- The script checks if the csv file exists and it can be opened, it has lat and lon columns, filter valid lat lon combination,  and checks that there are more than 0 valid lat and lon combination. The human should check that the script is working and that the output structure is what is expected based on the code.

* Scale: What problems might happen if the dataset becomes very large?
- If the dataset becomes very large, processing time of the script will increase.

## Authors

Contributors names and contact info

Randy C. Beros
rcberos@up.edu.ph

## Version History


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments
