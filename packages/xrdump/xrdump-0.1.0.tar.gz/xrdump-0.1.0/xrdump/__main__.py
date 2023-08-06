import xarray as xr
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Displays information about an xarray-openable dataset")
    parser.add_argument("path", type=str, help="path of dataset")
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    ds = xr.open_dataset(args.path)
    print(ds)

if __name__ == '__main__':
    main()
