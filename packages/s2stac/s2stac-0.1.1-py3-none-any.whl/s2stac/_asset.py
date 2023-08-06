from typing import Any
import pystac
from pystac.extensions.eo import Band, EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterBand, RasterExtension
from pathlib import Path


def add_asset(
    item: pystac.Item,
    asset_path: Path,
    asset_label: str,
    asset_description: str,
    asset_common_name: str,
    asset_nodata: float,
    asset_epsg: str,
    asset_geometry: dict[str, Any],
    asset_bbox: list[float],
    asset_shape: list[int],
    asset_transform: list[float],
) -> Band:
    asset = pystac.Asset(href=str(asset_path), media_type=pystac.MediaType.JPEG2000)
    # Add image to asset
    item.add_asset(asset_label, asset)
    # Add Band to asset
    asset_band = Band.create(
        name=asset_label,
        description=asset_description,
        common_name=asset_common_name,
    )
    eo_on_asset = EOExtension.ext(item.assets[asset_label])
    eo_on_asset.apply(bands=[asset_band])
    # Add Raster Band to asset
    asset_raster_band = RasterBand.create(nodata=asset_nodata)
    raster_on_asset = RasterExtension.ext(item.assets[asset_label], add_if_missing=True)
    raster_on_asset.apply(bands=[asset_raster_band])
    # Add Projection to asset
    proj_on_asset = ProjectionExtension.ext(
        item.assets[asset_label], add_if_missing=True
    )
    proj_on_asset.apply(
        epsg=asset_epsg,
        geometry=asset_geometry,
        bbox=asset_bbox,
        shape=asset_shape,
        transform=asset_transform,
    )
    return asset_band
