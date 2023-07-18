# Alaska Lightning Detection Network Gridding Toolkit
[![DOI](https://zenodo.org/badge/502487778.svg)](https://zenodo.org/badge/latestdoi/502487778)

## Overview
The Alaska Fire Service operates the ALDN to support fire management. The [historical lightning data](https://fire.ak.blm.gov/predsvcs/maps.php) is provided as a
csv where each row represents point data for each observed stroke. Currently this is the most comprehensive dataset of lightning publicly available for Alaska and there is
a need for a gridded product for climatological research. This toolkit was built to generate and update such a gridded lightning product. The toolkit contains two functions which can be used in either command line or implemented within a script. 

## Data Availability and Provenance
The raw (ungridded) [historical lightning data](https://fire.ak.blm.gov/predsvcs/maps.php) is publicly provided by the Alaska Fire Service. This archive provides the gridded lightning product generated by the grid_lib.py functions. 

### Details of Data
Many changes have been made to the lightning detection network which are described in README_BLM_Alaska_Historical_lightning.pdf - provided with the raw data at the link. These changes are mostly upgrades to the network which improve detection defficiency and coverage. For this reason, the data may not not be suitable for trend analysis. Notably, the system was overhauled in 2012 during which two sensor networks ran simultaneously. The new system, which covers 2012-Current, was not properly calibrated in its first year of operation. An investigation of the reported cloud-to-ground stroke amplitudes suggested that many of these strokes are misclassified cloud-to-cloud strokes. This is consistent with the parameter governing the number of station-detections required to report a stroke. This parameter was initially set to the minimum value which leads to oversensitivty. For this reason we drop all low amplitude positive strokes (<10kA) from BOTH the Impact systems and TOA datasets. 

## Computational Requirements

### Software Requirments
This library is entirely contained within Python. The environment to execute the gridding toolkit can be set up in conda with the provided requirements.txt.

### Memory and Runtime
This toolkit was last run on 7-17-2023 on a Windows 11 PC with an AMD Ryzen 9 3900x and 32GB of RAM. Total time to grid one year of data is under 10 seconds. Recommended to have at least 4GB of available RAM.

## Description of Code
The code is simple to implement, just copy or create a gridcells file with make_gridcells() and call grid() to transform csv stroke data to the grid.

### Functions:
- make_gridcells(): constructs and saves a gridcell file to the current working directory. Default grid is aligned to the ERA 5 grid.
- grid(): grids a single year of lightning data to the provided gridcell structure. Default will look for the pre-generated 'gridcells.gpkg' file in the current working directory.

### Example
See main.py for an example of a scripted application of this toolkit. The following is an example gridding the year 2016 from the conda interpreter.

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
### Details

## License
MIT License

Copyright (c) 2023 Joshua Hostler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## References
Alaska Interagency Coordination Center. (n.d.). Predictive services - maps/imagery/geospatial. AICC - Predictive Services - maps/imagery/geospatial. https://fire.ak.blm.gov/predsvcs/maps.php 
