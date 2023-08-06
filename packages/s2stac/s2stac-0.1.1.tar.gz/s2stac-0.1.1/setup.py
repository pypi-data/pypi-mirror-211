# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['s2stac']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.12.2,<5.0.0',
 'bokeh==2.4.2',
 'cfgrib>=0.9.10.3,<0.10.0.0',
 'dask>=2023.5.0,<2024.0.0',
 'distributed>=2023.5.0,<2024.0.0',
 'eccodes==1.2.0',
 'geopandas>=0.13.0,<0.14.0',
 'jinja2==3.0.3',
 'lxml>=4.9.2,<5.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.3,<2.0.0',
 'pygeoapi>=0.14.0,<0.15.0',
 'pygrib>=2.1.4,<3.0.0',
 'pystac-client>=0.6.1,<0.7.0',
 'pystac>=1.7.3,<2.0.0',
 'rasterio>=1.3.6,<2.0.0',
 'rioxarray>=0.14.1,<0.15.0',
 'shapely==1.8.5',
 'stackstac>=0.4.3,<0.5.0',
 'xarray>=2023.4.2,<2024.0.0']

setup_kwargs = {
    'name': 's2stac',
    'version': '0.1.1',
    'description': 'Create a STAC from local S2 data.',
    'long_description': '# s2stac\n\nEasily access many Sentinel-2 safe folders from a convenient xarray Dataset.\n\n## Purpose\n\nThe purpose of this library is to create on-the-fly STAC from a list Sentinel-2 products in the form of SAFE folders and provide a xarray Dataset to easily access the main Sentinel-2 bands and more!\n\nAccessible information includes:\n- all bands from the IMG_DATA folder (B01, B02, ..., B11)\n- all viewing/sun zenith/azimuth angles.\n- all detector footprints (for each band)\n- ECMWF data (msl, tco3, ...)\n\n## How it works\n\ns2stac uses the stackstac library internally to interogate a static STAC database created on the fly with pystac.\nThe database can be persisted so the user does not need to build it everytime.\n\n## Installation\n\nThis library requires Python 3.10 or higher.\n\nThis library also requires the eccodes library (version 2.16.0) to be able to parse the GRIB ECMWF dataset containing the meteorological data associated with each tile.\nYou can install it on Ubuntu with the following command:\n```bash\nsudo apt-get install libeccodes-dev\n```\n\nNow you can simply install s2stac with:\n```bash\npip install s2stac\n```\n\n## Usage\n\n```python\nfrom pathlib import Path\nfrom s2stac import stacify\n\nsafe_folders = list(Path("/path/to/your/safe/folders").glob("*.SAFE"))\n\nstack = stacify(safe_folders)\nstack\n```\n\nExemple of output:\n```bash\n<xarray.DataArray \'stackstac-67b9dd4d3bf2316dde72ffa86206dab6\' (time: 1,\n                                                                band: 59,\n                                                                y: 12352,\n                                                                x: 12352)>\ndask.array<where, shape=(1, 59, 12352, 12352), dtype=float64, chunksize=(1, 1, 5000, 5000), chunktype=numpy.ndarray>\nCoordinates: (12/16)\n  * time                 (time) datetime64[ns] 2023-06-02T15:00:42.812526\n    id                   (time) <U60 \'S2B_MSIL2A_20190222T095029_N0211_R079_T...\n  * band                 (band) <U16 \'AOT\' \'B02\' ... \'VIEW_ZENITH_B12\'\n  * x                    (x) float64 4.931e+05 4.931e+05 ... 6.166e+05 6.166e+05\n  * y                    (y) float64 6.709e+06 6.709e+06 ... 6.585e+06 6.585e+06\n    gsd                  int64 10\n    ...                   ...\n    raster:bands         object {\'nodata\': 0}\n    proj:geometry        object {\'type\': \'Polygon\', \'coordinates\': (((499980....\n    common_name          (band) <U16 \'AOT\' \'B02\' ... \'VIEW_ZENITH_B12\'\n    center_wavelength    object None\n    full_width_half_max  object None\n    epsg                 <U10 \'EPSG:32634\'\n```\n\n## License\n\nMIT\n\n\n## Author\n\nPierre Louvart - plouvart@argans.eu\n\n## Credit\n\ngjoseph92, the creator of [https://stackstac.readthedocs.io/en/latest/](stackstac)\n\n',
    'author': 'Pierre Louvart',
    'author_email': 'pierre.louvart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.5,<4.0.0',
}


setup(**setup_kwargs)
