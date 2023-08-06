# s2stac

Easily access many Sentinel-2 safe folders from a convenient xarray Dataset.

## Purpose

The purpose of this library is to create on-the-fly STAC from a list Sentinel-2 products in the form of SAFE folders and provide a xarray Dataset to easily access the main Sentinel-2 bands and more!

Accessible information includes:
- all bands from the IMG_DATA folder (B01, B02, ..., B11)
- all viewing/sun zenith/azimuth angles.
- all detector footprints (for each band)
- ECMWF data (msl, tco3, ...)

## How it works

s2stac uses the stackstac library internally to interogate a static STAC database created on the fly with pystac.
The database can be persisted so the user does not need to build it everytime.

## Installation

This library requires Python 3.10 or higher.

This library also requires the eccodes library (version 2.16.0) to be able to parse the GRIB ECMWF dataset containing the meteorological data associated with each tile.
You can install it on Ubuntu with the following command:
```bash
sudo apt-get install libeccodes-dev
```

Now you can simply install s2stac with:
```bash
pip install s2stac
```

## Usage

```python
from pathlib import Path
from s2stac import stacify

safe_folders = list(Path("/path/to/your/safe/folders").glob("*.SAFE"))

stack = stacify(safe_folders)
stack
```

Exemple of output:
```bash
<xarray.DataArray 'stackstac-67b9dd4d3bf2316dde72ffa86206dab6' (time: 1,
                                                                band: 59,
                                                                y: 12352,
                                                                x: 12352)>
dask.array<where, shape=(1, 59, 12352, 12352), dtype=float64, chunksize=(1, 1, 5000, 5000), chunktype=numpy.ndarray>
Coordinates: (12/16)
  * time                 (time) datetime64[ns] 2023-06-02T15:00:42.812526
    id                   (time) <U60 'S2B_MSIL2A_20190222T095029_N0211_R079_T...
  * band                 (band) <U16 'AOT' 'B02' ... 'VIEW_ZENITH_B12'
  * x                    (x) float64 4.931e+05 4.931e+05 ... 6.166e+05 6.166e+05
  * y                    (y) float64 6.709e+06 6.709e+06 ... 6.585e+06 6.585e+06
    gsd                  int64 10
    ...                   ...
    raster:bands         object {'nodata': 0}
    proj:geometry        object {'type': 'Polygon', 'coordinates': (((499980....
    common_name          (band) <U16 'AOT' 'B02' ... 'VIEW_ZENITH_B12'
    center_wavelength    object None
    full_width_half_max  object None
    epsg                 <U10 'EPSG:32634'
```

## License

MIT


## Author

Pierre Louvart - plouvart@argans.eu

## Credit

gjoseph92, the creator of [https://stackstac.readthedocs.io/en/latest/](stackstac)

