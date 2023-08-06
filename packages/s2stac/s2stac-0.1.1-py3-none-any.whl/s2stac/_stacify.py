import pystac
from pathlib import Path
import xarray as xr
import stackstac
import numpy as np


from s2stac._catalog import create_stac_catalog


def stacify(
    safe_folders: list[Path],
    catalog_folder: Path | None = None,
    # Include flags
    include_img_data: bool = True,
    include_qi_data: bool = True,
    include_aux_data: bool = True,
    include_footprint: bool = True,
    include_cloud_proba: bool = True,
    include_ecmwf: bool = True,
    include_mtd_tl: bool = True,
    # Stackstac parameters
    epsg: int | None = None,
    **kwargs,
) -> pystac.Catalog:
    catalog = create_stac_catalog(
        safe_folders=safe_folders,
        catalog_folder=catalog_folder,
        include_img_data=include_img_data,
        include_qi_data=include_qi_data,
        include_aux_data=include_aux_data,
        include_footprint=include_footprint,
        include_cloud_proba=include_cloud_proba,
        include_ecmwf=include_ecmwf,
        include_mtd_tl=include_mtd_tl,
    )
    items = list(catalog.get_all_items())

    if len(set(item.properties["proj:epsg"] for item in items)) > 1 and epsg is None:
        epsg = items[0].properties["proj:epsg"]
    stack = stackstac.stack(items, epsg=epsg, chunksize=(5000, 5000), **kwargs)

    # Turn no data (0) into NaNs
    stack = xr.where(stack, stack, np.nan)
    return stack
