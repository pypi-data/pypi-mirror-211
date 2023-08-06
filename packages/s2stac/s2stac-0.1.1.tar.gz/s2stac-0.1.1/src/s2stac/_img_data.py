import pystac
from pystac.extensions.eo import Band
from pathlib import Path
import rioxarray

from ._asset import add_asset


def add_img_data_var(
    item: pystac.Item,
    img_data_var_path: Path,
    img_data_var_label: str,
    img_data_var_description: str,
    tmp_folder: Path,
) -> Band:
    img_data_var_da = rioxarray.open_rasterio(img_data_var_path)

    return add_asset(
        item=item,
        asset_path=img_data_var_path,
        asset_label=img_data_var_label,
        asset_description=img_data_var_description,
        asset_common_name=img_data_var_label,
        asset_nodata=0,
        asset_epsg=f"EPSG:{img_data_var_da.rio.crs.to_epsg()}",
        asset_geometry=item.geometry,
        asset_bbox=item.bbox,
        asset_shape=img_data_var_da.shape[-2:],
        asset_transform=list(img_data_var_da.rio.transform()),
    )


def add_img_data_bands(
    item: pystac.Item,
    img_data_folder: Path,
    tmp_folder: Path,
) -> list[Band]:
    return [
        add_img_data_var(
            item=item,
            img_data_var_path=list(
                img_data_folder.glob(f"*{img_data_res}*/*{img_data_label}*.jp2")
            )[0],
            img_data_var_label=img_data_label,
            img_data_var_description=img_data_description,
            tmp_folder=tmp_folder,
        )
        for img_data_res, img_data_label, img_data_description in [
            ("10", "AOT", ""),
            ("10", "B02", ""),
            ("10", "B03", ""),
            ("10", "B04", ""),
            ("10", "B08", ""),
            ("10", "TCI", ""),
            ("10", "WVP", ""),
            ("20", "B05", ""),
            ("20", "B06", ""),
            ("20", "B07", ""),
            ("20", "B8A", ""),
            ("20", "B11", ""),
            ("20", "B12", ""),
            ("20", "SCL", ""),
            ("60", "B01", ""),
            ("60", "B09", ""),
        ]
    ]
