import pystac
from pystac.extensions.eo import Band
from pathlib import Path
import rioxarray
import xarray as xr

from ._asset import add_asset


def add_ecmwf_var(
    item: pystac.Item,
    ecmwft_var_label: str,
    ecmwft_var_da: xr.DataArray,
    target_da: xr.DataArray,
    tmp_folder: Path,
) -> Band:
    ecmwft_var_path = tmp_folder / f"{ecmwft_var_label}.tiff"
    if ecmwft_var_path.exists():
        ecmwft_var_da = rioxarray.open_rasterio(ecmwft_var_path)
    else:
        ecmwft_var_da = ecmwft_var_da.rename({"latitude": "y", "longitude": "x"})
        ecmwft_var_da = ecmwft_var_da.rio.write_crs("epsg:4326")
        ecmwft_var_da = ecmwft_var_da.transpose("y", "x")
        ecmwft_var_da = ecmwft_var_da.rio.write_nodata(
            ecmwft_var_da.attrs["GRIB_missingValue"]
        )
        ecmwft_var_da = ecmwft_var_da.rio.reproject(
            target_da.rio.crs,
            shape=ecmwft_var_da.shape,
        )
        ecmwft_var_da.rio.to_raster(ecmwft_var_path)

    return add_asset(
        item=item,
        asset_path=ecmwft_var_path,
        asset_label=ecmwft_var_label,
        asset_description=ecmwft_var_label,
        asset_common_name=ecmwft_var_label,
        asset_nodata=0,
        asset_epsg=f"EPSG:{ecmwft_var_da.rio.crs.to_epsg()}",
        asset_geometry=item.geometry,
        asset_bbox=item.bbox,
        asset_shape=ecmwft_var_da.shape[-2:],
        asset_transform=list(ecmwft_var_da.rio.transform()),
    )


def add_ecmwf(
    item: pystac.Item,
    ecmwft_path: Path,
    target_da: xr.DataArray,
    tmp_folder: Path,
) -> list[Band]:
    tmp_folder = tmp_folder / "ecmwft"
    tmp_folder.mkdir(exist_ok=True)

    ecmwft_da = xr.open_dataset(ecmwft_path, engine="cfgrib")
    return [
        add_ecmwf_var(
            item=item,
            ecmwft_var_label=ecmwft_var_label,
            ecmwft_var_da=ecmwft_da[ecmwft_var_label],
            target_da=target_da,
            tmp_folder=tmp_folder,
        )
        for ecmwft_var_label in ecmwft_da.data_vars
        if ecmwft_var_label in ["msl", "tco3", "tcwv"]
    ]
