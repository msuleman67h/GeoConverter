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

| Short |     Long    | Type          | Default | Description                                                                                        | Compulsory |
|:-----:|:-----------:|---------------|:-------:|----------------------------------------------------------------------------------------------------|------------|
| -h    |  --help     | String        |         | show this help message and exit                                                                    | No         |
| -i    |  --input    | String        |         | Input file namepath with extension                                                                 | Yes        |
| -o    | --output    | String        |         |                                                                                                    | Yes        |
| -m    | --mode      | String        | xyz     | Set the output mode ("lla" or "xyz")                                                               | No         |
| -w    | --waypoints | String \| Int | 10      | Sets the number of waypoints created. "All" will use all points available                            |            |
|       | --header    | Boolean       | False   | Set to True if there is a 13 row header, as seen with data from GPS                                | No         |
| -t    | --tab       | Boolean       | False   | Set to True if file is tab seperated (.tsv)                                                        | No         |
| -s    | --spaced    | Boolean       | False   | Set to True for a blank space after every row in the output                                        | No         |
| -n    | --normalize | Boolean       | False   | Set to True for normalized data                                                                    | No         |
|       | --normvalue | Float         | 20.0    | If normalizing this is the number normalized to                                                    | No         |
| -r    | --rawoutput | Boolean       | False   | Set to True if you want the raw output, otherwise the data will be the offset from the first point | No         |
| -v    | --velocity  | Float         |  5.0    | Value that will be used for velocity                                                               | No         |
| -a    | --angle     | Float         | 0.0     | Value that will be used for angle                                                                  | No         |

OUTPUTS (Two Possible):
- UTM ->   X(Easting)[m] Y(Northing)[m] Z(Altitude)[m] ANGLE[deg] Velocity[m/s]
- WGS84 -> Latitude[deg] Longitude[deg] Z(Altitude)[m] ANGLE[deg] Velocity[m/s]

### Getting Started
If you have Python 3.9, the script should run without any issues

To create an normalized to 50 in xyz output with an angle of 12 and a velocity of 17 with 25 waypoints:

```
foo@bar:~$ cd [Location_of_py_file]
Location_of_py_file> python gps_csv_conversion.py -i [Input_file_path] -o[Output_file_path] -n 1 --normvalue 50 -a 12 -v 17 -w 25
```
**Example:**

```
> gps_csv_converter.py -i mrc_sep_02/mrc_straight_line.csv -o mrc_sep_02/xyz_mrc_straight_line.csv -n 0 -w "all" -r 1 -v 0
```
				



