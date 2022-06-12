from grid import grid, make_gridcells

def main():
    gridcells_path = make_gridcells()
    grid(fn=r'', year=2016, gridcells_path=gridcells_path)

if __name__ == '__main__':
    main()