# LLA to XYZ GPS Converter

## Installation 
Assumptions for the gps_csv_conversion.py file are:

### Prerequisite
- Python Version <= 3.9.1 
- numpy 1.20.3
- Pandas 1.2.4
- utm 0.7.0

### Input 
 - Single CSV at a time

## Arguments and Usage
```
gps_csv_conversion.py [-h] -i INPUT -o OUTPUT [-m MODE] [-w WAYPOINTS] [--header HEADER] [-t TAB] [-s SPACED]
                             [-r RAWOUTPUT] [-n NORMALIZE] [--normvalue NORMVALUE] [-v VELOCITY] [-a ANGLE]
```

| Short |     Long    | Type    | Default | Description                     | Compulsory |
|:------|:------------|:--------|:--------|:--------------------------------|:-----------|
| -h    |  --help     | String  |         | show this help message and exit | No         |
| -i    |  --input    | String  |         |                                 | Yes        |
| -o    |             | String  |         |                                 |            |
| -m    |             | String  |         |                                 |            |
|       | --header    | Boolean |         |                                 |            |
| -t    |             | Boolean |         |                                 |            |
| -s    |             |         |         |                                 |            |
| -n    |             |         |         |                                 |            |
|       | --normvalue |         |         |                                 |            |
|       |             |         |         |                                 |            |
|       |             |         |         |                                 |            |

OUTPUTS(Two Possible):
	UTM Zone 17N->   X(Easting)[m] Y(Northing)[m] Z(Altitude)[m] ANGLE[deg] Velocity[m/s]
	Latitude[deg] Longitude[deg] Z(Altitude)[m] ANGLE[deg] Velocity[m/s]


						
If you have Python 3.9, the script should run without any issues


Example:
				.\ > cd [Location_of_py_file]
				
To create an normalized to 50 in xyz output with an angle of 12 and a velocity of 17 with 25 waypoints:
Location_of_py_file> python gps_csv_conversion.py -i [Input_file_path] -o[Output_file_path] -n 1 --normvalue 50 -a 12 -v 17 -w 25

> -i mrc_sep_02/mrc_straight_line.csv -o mrc_sep_02/xyz_mrc_straight_line.csv -n 0 -w "all" -r 1 -v 0