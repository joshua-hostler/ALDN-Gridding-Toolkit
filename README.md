# Alaska Lightning Detection Network Gridding Toolkit
This is a small toolkit for updating the existing gridded lightning product with new data. This
toolkit contains two functions which can be used in either command line or implemented within a script. 
### Functions:
- make_gridcells(): constructs and saves a gridcell file to the current working directory. Default grid is aligned to the ERA 5 grid.
- grid(): grids a single year of lightning data to the provided gridcell structure. Default will look for the pre-generated 'gridcells.csv' file in the current working directory.
## Instructions
For an example of a scripted application of this toolkit see main.

### Command Line:

Import functions:
```python
from grid_lib import make_gridcells, grid
```

Make gridcells:
```python
gridcells_path = make_gridcells()
```

Grid lightning:
```python
grid(fn=fn, year='2016', gridcells_fn=gridcells_path)
```