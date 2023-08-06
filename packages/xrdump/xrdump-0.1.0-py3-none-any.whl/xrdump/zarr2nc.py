import xarray as xr
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Converts zarr to netcdf")
    parser.add_argument("path", type=str, help="path of input zarr dataset")
    parser.add_argument("output", type=str, help="path of output netcdf")
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    ds = xr.open_zarr(args.path)
    ds.to_netcdf(args.output)

if __name__ == '__main__':
    main()
