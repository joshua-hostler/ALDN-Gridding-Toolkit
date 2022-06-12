import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import geopandas as gpd
from datetime import datetime
from pytz import timezone
import sparse
import math
import shapely.geometry
import os

def grid(fn, year, datetime_format_string='%m/%d/%Y %X', gridcells_fn='gridcells.gpkg', return_ds=False):
    '''
    Tool for updating gridded lightning dataset from the Alaska Lightning Detection Network (ALDN).
    :param fn: Filename of ALDN csv
    :param year: Year to grid
    :param datetime_format_string: Format string with which to parse datetime strings.
    :param gridcells_fn: Filename of gridcells csv. Default points to pre-generated gridcells. See make_gridcells() to
    create a custom grid.
    :return: DataSet of gridded lightning if True; else, None
    '''
    # Read in lightning csv as a DataFrame, and grid cells as a GeoDataFrame.
    cwd = os.getcwd()
    df = pd.read_csv(fn)
    gdf_gridcells = gpd.read_file(os.path.join(cwd, gridcells_fn))
    cell_shape = gdf_gridcells['geometry'].shape[0]
    whys = gdf_gridcells['lat'].unique()
    exes = gdf_gridcells['lon'].unique()

    # Clean lightning DataFrame.
    df = df.drop(df[df['STROKETYPE']=='CLOUD_STROKE'].index)
    df.LONGITUDE = df.LONGITUDE % 360

    # Parse stroke time of lightning DataFrame and create a column of dates.
    df['UTCDATETIME'] = df['UTCDATETIME'].apply(lambda x: datetime.strptime(x, datetime_format_string))
    df['day'] = df['UTCDATETIME'].dt.date

    # Create GeoDataFrame from lightning DataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGITUDE, df.LATITUDE))
    gdf = gdf.set_index(pd.DatetimeIndex(gdf['day']))
    gdf = gdf.loc[year]

    # Create list of unique days
    dates = gdf['day'].unique()
    dates = np.array(dates, dtype='datetime64')

    # Create array of indexes to dates.
    idxs = np.arange(np.shape(dates)[0])

    # Create empty sparse array with the shape of a flattened array of shape (day, lat, lon).
    s = sparse.COO(coords=[0], data=[0], shape=cell_shape*np.shape(dates)[0])

    for idx in idxs:
        # Get subset of lightning GeoDataFrame for specific day
        gdfn = gdf.loc[dates[idx]]
        print('gridding: ', dates[idx])
        if isinstance(gdfn, pd.Series):
            gdfn = gpd.GeoDataFrame(pd.DataFrame(gdfn).transpose(), geometry='geometry')
        merged = gpd.sjoin(gdfn, gdf_gridcells, how='left')
        ids = np.array(merged['OBJECTID'])
        vals, counts = np.unique(ids, return_counts=True)
        divs = np.repeat(counts, counts)
        merged['count'] = 1 / divs
        dissolved = merged.dissolve(by='index_right', aggfunc='sum')
        sn = sparse.COO(coords=np.array(dissolved.index + cell_shape * idx, dtype='int64'),
                        data=dissolved['count'].values, shape=cell_shape * np.shape(dates)[0])
        s = sparse.elemwise(np.add, s, sn)

    a = s.todense()
    fn_out = 'gridded_lightning_' +  year + r'.nc'
    path_out = os.path.join(cwd, fn_out)
    midx = pd.MultiIndex.from_product([dates, whys, exes], names=['date', 'lat', 'lon'])
    df = pd.DataFrame(data=a, index=midx, columns=['strokes'])
    ds = xr.Dataset.from_dataframe(df)
    ds.to_netcdf(path_out)
    if return_ds: return ds

def make_gridcells(fn=r'gridcells.gpkg', width=0.25, xmin=171, ymin=46, xmax=261, ymax=72, return_df=False):
    '''
    Generates a csv of gridcells for use in grid() function. A pre-generated gridcell file as generated with the
    defaults of this function is provided with the ALDN Gridding Toolkit.
    :param fn: Name of output gridcells file
    :param width: Width of gridcells.
    :param xmin: Minimum longitude bound of gridcells.
    :param ymin: Minimum latitude bound of gridcells.
    :param xmax: Maximum longitude bound of gridcells.
    :param ymax: Maximum latitude bound of gridcells.
    :return: Path to csv and gridcells DataFrame if True; else, returns None
    '''

    grid_cells = []
    exes = []
    whys = []
    print('Building grid_cells and coordinate sets.')
    for x0 in np.arange(xmin, xmax + width, width):
        exes.append(x0)
    for y0 in np.arange(ymin, ymax + width, width):
        whys.append(y0)
        for x0 in np.arange(xmin, xmax + width, width):
            grid_cells.append(shapely.geometry.box(x0 - 0.125, y0 - 0.125, x0 + 0.125, y0 + 0.125))

    midx = pd.MultiIndex.from_product([whys, exes], names=['lat', 'lon'])
    cell = gpd.GeoDataFrame(grid_cells, columns=['geometry'], index=midx)
    cell.reset_index()
    path_out = os.path.join(os.getcwd(), fn)
    cell.to_file(path_out, driver='GPKG')
    if return_df:
        return path_out, cell

    return path_out