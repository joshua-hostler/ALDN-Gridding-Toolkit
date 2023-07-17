from grid_lib import grid, make_gridcells

def main():
    gridcells_path = make_gridcells()
    grid(fn=r'Z:\PyProj\ALDN Gridding Toolkit\Historical_Lightning_2012_2022_TOA_AlaskaAlbersNAD83.txt', year='2016', gridcells_fn=gridcells_path)

if __name__ == '__main__':
    main()