# CSV numeric data handler
This package allow to retrive numeric data from CSV table.

## Support feature

* Interpolate two column and take number between 
* Take column data relative to another column by index
* And more usefull function for me 

## Installation

Using pip, you can install:
	
	pip install data-handler-csv

Or using setup.py 

## Example of usage

Need .csv format data with first row be like 'header'

```python
import DataHandler as dh

df = dh.DataHandler('path/file_name.csv')
# Data should be stored in column

column_values = df.get_column('column_name')
#Take all column with that name in 'header'

```
Can take a intermediate value from column relative to another column 
```python
import DataHandler as dh
import numpy as np

df = dh.DataHandler('path/file_name.csv')

time_values = np.arange(0, 11, 1)
# WORK ONLY WITH NUMPY ARRAY IN ELEMENTS PARAMETER
force = df.get_column('force', 'time', time_values, inter_value=True)

```

## Requirements

	numpy == 1.20.2
	pandas == 1.2.4
	scipy == 1.6.3



