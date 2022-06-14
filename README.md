# Alaska Lightning Detection Network Gridding Toolkit
The Alaska Fire Service owns and operates the ALDN to support fire management. The [historical lightning data](https://fire.ak.blm.gov/predsvcs/maps.php) is provided as a
csv where each row represents point data for each observed stroke. Currently this is the most comprehensive dataset of lightning in Alaska and there is
a need for a gridded product of the dataset for climatological research. This toolkit was built for updating the existing gridded lightning product with new data. 
The toolkit contains two functions which can be used in either command line or implemented within a script. 
### Functions:
- make_gridcells(): constructs and saves a gridcell file to the current working directory. Default grid is aligned to the ERA 5 grid.
- grid(): grids a single year of lightning data to the provided gridcell structure. Default will look for the pre-generated 'gridcells.gpkg' file in the current working directory.
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

Grid lightning for 2016:
```python
grid(fn=r'Historical_Lightning_2012_2020_TOA_AlaskaAlbersNAD83.txt', year='2016', gridcells_fn=gridcells_path)
```