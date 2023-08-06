import pystac
from pystac.extensions.eo import Band
from pathlib import Path
import xarray as xr
import rasterio
import rasterio.features
import rioxarray
import numpy as np
import geopandas as gpd

from ._asset import add_asset


def rasterize_footprint(
    footprint_path: Path,
    target_da: xr.DataArray,
) -> xr.DataArray:
    gdf = gpd.read_file(footprint_path, driver="GML")
    return xr.DataArray(
        rasterio.features.rasterize(
            shapes=[
                (row["geometry"], int(row["gml_id"].split("-")[-2]))
                for _, row in gdf.iterrows()
            ],
            transform=target_da.rio.transform(),
            out_shape=target_da.shape[-2:],
            fill=0,
            dtype=np.uint8,
        ),
        coords={
            "y": target_da.y,
            "x": target_da.x,
        },
        dims=["y", "x"],
    ).rio.write_crs(target_da.rio.crs)


def add_footprint(
    item: pystac.Item,
    footprint_path: Path,
    footprint_label: str,
    footprint_description: str,
    target_da: xr.DataArray,
    tmp_folder: Path,
) -> Band:
    if footprint_path.suffix == ".gml":
        tmp_footprint_path = tmp_folder / footprint_path.with_suffix(".jp2").name
        if tmp_footprint_path.exists():
            footprint_da = rioxarray.open_rasterio(tmp_footprint_path)
        else:
            footprint_da = rasterize_footprint(
                footprint_path=footprint_path,
                target_da=target_da,
            )
            footprint_da.rio.to_raster(tmp_footprint_path)
            footprint_da = rioxarray.open_rasterio(tmp_footprint_path)
        footprint_path = tmp_footprint_path
    else:
        footprint_da = rioxarray.open_rasterio(footprint_path)

    return add_asset(
        item=item,
        asset_path=footprint_path,
        asset_label=footprint_label,
        asset_description=footprint_description,
        asset_common_name=footprint_label,
        asset_nodata=0,
        asset_epsg=f"EPSG:{footprint_da.rio.crs.to_epsg()}",
        asset_geometry=item.geometry,
        asset_bbox=item.bbox,
        asset_shape=footprint_da.shape[-2:],
        asset_transform=list(footprint_da.rio.transform()),
    )


def add_footprints(
    item: pystac.Item,
    qi_folder: Path,
    target_da_10m: xr.DataArray,
    target_da_20m: xr.DataArray,
    target_da_60m: xr.DataArray,
    tmp_folder: Path,
) -> list[Band]:
    return [
        add_footprint(
            item=item,
            footprint_path=(
                list(qi_folder.glob(f"*{footprint_label}*.jp2"))
                + list(qi_folder.glob(f"*{footprint_label}*.gml"))
            )[0],
            footprint_label=footprint_label,
            footprint_description=footprint_description,
            target_da=target_da,
            tmp_folder=tmp_folder,
        )
        for footprint_res, footprint_label, footprint_description, target_da in [
            ("60", "MSK_DETFOO_B01", "", target_da_60m),
            ("10", "MSK_DETFOO_B02", "", target_da_10m),
            ("10", "MSK_DETFOO_B03", "", target_da_10m),
            ("10", "MSK_DETFOO_B04", "", target_da_10m),
            ("20", "MSK_DETFOO_B05", "", target_da_20m),
            ("20", "MSK_DETFOO_B06", "", target_da_20m),
            ("20", "MSK_DETFOO_B07", "", target_da_20m),
            ("10", "MSK_DETFOO_B08", "", target_da_10m),
            ("20", "MSK_DETFOO_B8A", "", target_da_20m),
            ("60", "MSK_DETFOO_B09", "", target_da_60m),
            ("20", "MSK_DETFOO_B10", "", target_da_20m),
            ("20", "MSK_DETFOO_B11", "", target_da_20m),
            ("20", "MSK_DETFOO_B12", "", target_da_20m),
        ]
    ]


def add_msk_cldprb(
    item: pystac.Item,
    msk_cldprb_path: Path,
    msk_cldprb_label: str,
    msk_cldprb_description: str,
    tmp_folder: Path,
) -> Band:
    msk_cldprb_da = rioxarray.open_rasterio(msk_cldprb_path)

    return add_asset(
        item=item,
        asset_path=msk_cldprb_path,
        asset_label=msk_cldprb_label,
        asset_description=msk_cldprb_description,
        asset_common_name=msk_cldprb_label,
        asset_nodata=0,
        asset_epsg=f"EPSG:{msk_cldprb_da.rio.crs.to_epsg()}",
        asset_geometry=item.geometry,
        asset_bbox=item.bbox,
        asset_shape=msk_cldprb_da.shape[-2:],
        asset_transform=list(msk_cldprb_da.rio.transform()),
    )


def add_qi_data(
    item: pystac.Item,
    qi_folder: Path,
    target_da_10m: xr.DataArray,
    target_da_20m: xr.DataArray,
    target_da_60m: xr.DataArray,
    tmp_folder: Path,
    include_footprint: bool = True,
    include_cloud_proba: bool = True,
) -> list[Band]:
    bands = []
    if include_cloud_proba:
        bands += [
            add_msk_cldprb(
                item=item,
                msk_cldprb_path=qi_folder / "MSK_CLDPRB_20m.jp2",
                msk_cldprb_label="MSK_CLDPRB",
                msk_cldprb_description="Coud probability [0-255]",
                tmp_folder=tmp_folder,
            )
        ]
    if include_footprint:
        bands += add_footprints(
            item=item,
            qi_folder=qi_folder,
            target_da_10m=target_da_10m,
            target_da_20m=target_da_20m,
            target_da_60m=target_da_60m,
            tmp_folder=tmp_folder,
        )
    return bands
