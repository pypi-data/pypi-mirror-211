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
    'version': '0.1.0',
    'description': 'Create a STAC from local S2 data.',
    'long_description': '# s2stac\n\nCreate a STAC from Sentinel-2 data.\n\n## Purpose\n\nThe purpose of this library is to create on-the-fly STAC from a list Sentinel-2 products in the form of SAFE folders.\n\n\n\n',
    'author': 'Pierre Louvart',
    'author_email': 'pierre.louvart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.10.5',
}


setup(**setup_kwargs)
