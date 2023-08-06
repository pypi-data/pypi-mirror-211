import pystac
from pystac.extensions.eo import Band
from pathlib import Path
import xarray as xr
import rioxarray
import numpy as np
from bs4 import BeautifulSoup
from bs4.element import Tag

from ._asset import add_asset


def parse_xml_array(tag: Tag) -> np.array:
    return np.array(
        [list(map(float, i.string.split())) for i in tag.Values_List.find_all("VALUES")]
    )


def mtd_tl_to_dataset(
    mtd_tl_path: Path,
    target_da: xr.DataArray,
) -> xr.Dataset:
    soup = BeautifulSoup(open(mtd_tl_path, "r").read(), features="xml")

    xmin = float(
        soup.Tile_Geocoding.findAll("Geoposition", {"resolution": "10"})[0].ULX.string
    )
    xmax = xmin + float(
        soup.Tile_Geocoding.findAll("Size", {"resolution": "10"})[0].NCOLS.string
    ) * float(
        soup.Tile_Geocoding.findAll("Geoposition", {"resolution": "10"})[0].XDIM.string
    )

    ymin = float(
        soup.Tile_Geocoding.findAll("Geoposition", {"resolution": "10"})[0].ULY.string
    )
    ymax = ymin + float(
        soup.Tile_Geocoding.findAll("Size", {"resolution": "10"})[0].NROWS.string
    ) * float(
        soup.Tile_Geocoding.findAll("Geoposition", {"resolution": "10"})[0].YDIM.string
    )

    sun_zenith_data = parse_xml_array(soup.Tile_Angles.Sun_Angles_Grid.Zenith)
    sun_azimuth_data = parse_xml_array(soup.Tile_Angles.Sun_Angles_Grid.Azimuth)

    nb_cols, nb_rows = sun_zenith_data.shape
    # Should we correct the offset or not?
    xoffset = 0  # (xmax - xmin) / (nb_cols + 1)
    yoffset = 0  # (ymax - ymin) / (nb_rows + 1)
    x = np.linspace(xmin + xoffset, xmax - xoffset, nb_cols)
    y = np.linspace(ymin + yoffset, ymax - yoffset, nb_rows)

    sun_zenith_array = xr.DataArray(
        sun_zenith_data, coords={"y": y, "x": x}, dims=["y", "x"]
    )
    sun_azimuth_array = xr.DataArray(
        sun_azimuth_data, coords={"y": y, "x": x}, dims=["y", "x"]
    )

    mean_sun_zenith = float(soup.Mean_Sun_Angle.ZENITH_ANGLE.string)
    mean_sun_azimuth = float(soup.Mean_Sun_Angle.AZIMUTH_ANGLE.string)

    bands_data = dict(
        sorted(
            {
                (
                    int(grid["bandId"]),
                    grid["detectorId"],
                ): (
                    parse_xml_array(grid.Zenith),
                    parse_xml_array(grid.Azimuth),
                )
                for grid in soup.Tile_Angles.find_all("Viewing_Incidence_Angles_Grids")
            }.items()
        )
    )
    band_ids = list(sorted(set([k[0] for k in bands_data.keys()])))
    detector_ids = list(sorted(set([k[1] for k in bands_data.keys()])))
    band_labels = list(map(lambda s: f"B{s:02d}", band_ids))

    bands_zenith_array = xr.DataArray(
        np.stack([[bands_data[(j, i)][0] for i in detector_ids] for j in band_ids]),
        coords={
            "band": band_labels,
            "detector": detector_ids,
            "y": y,
            "x": x,
        },
        dims=["band", "detector", "y", "x"],
    )
    bands_azimuth_array = xr.DataArray(
        np.stack([[bands_data[(j, i)][1] for i in detector_ids] for j in band_ids]),
        coords={
            "band": band_labels,
            "detector": detector_ids,
            "y": y,
            "x": x,
        },
        dims=["band", "detector", "y", "x"],
    )

    bands_mean_data = dict(
        sorted(
            {
                int(mean_viewing_angles["bandId"]): (
                    float(mean_viewing_angles.ZENITH_ANGLE.string),
                    float(mean_viewing_angles.AZIMUTH_ANGLE.string),
                )
                for mean_viewing_angles in (
                    soup.Mean_Viewing_Incidence_Angle_List.find_all(
                        "Mean_Viewing_Incidence_Angle"
                    )
                )
            }.items()
        )
    )
    bands_mean_zenith_array = xr.DataArray(
        [v[0] for v in bands_mean_data.values()],
        coords={
            "band": band_labels,
        },
        dims=["band"],
    )
    bands_mean_azimuth_array = xr.DataArray(
        [v[1] for v in bands_mean_data.values()],
        coords={
            "band": band_labels,
        },
        dims=["band"],
    )

    return xr.Dataset(
        {
            "view_mean_zenith": bands_mean_zenith_array,
            "view_mean_azimuth": bands_mean_azimuth_array,
            "view_zenith": bands_zenith_array,
            "view_azimuth": bands_azimuth_array,
            "sun_mean_zenith": mean_sun_zenith,
            "sun_mean_azimuth": mean_sun_azimuth,
            "sun_zenith": sun_zenith_array,
            "sun_azimuth": sun_azimuth_array,
        }
    ).rio.write_crs(target_da.rio.crs)


def add_viewing_azimuth_band(
    item: pystac.Item,
    viewing_azimuth_band_label: str,
    viewing_azimuth_band_da: xr.DataArray,
    tmp_folder: Path,
) -> Band:
    viewing_azimuth_band_path = tmp_folder / f"{viewing_azimuth_band_label}.tiff"
    if viewing_azimuth_band_path.exists():
        viewing_azimuth_band_da = rioxarray.open_rasterio(viewing_azimuth_band_path)
    else:
        viewing_azimuth_band_da.rio.to_raster(viewing_azimuth_band_path)

    return add_asset(
        item=item,
        asset_path=viewing_azimuth_band_path,
        asset_label=viewing_azimuth_band_label,
        asset_description=viewing_azimuth_band_label,
        asset_common_name=viewing_azimuth_band_label,
        asset_nodata=0,
        asset_epsg=f"EPSG:{viewing_azimuth_band_da.rio.crs.to_epsg()}",
        asset_geometry=item.geometry,
        asset_bbox=item.bbox,
        asset_shape=viewing_azimuth_band_da.shape[-2:],
        asset_transform=list(viewing_azimuth_band_da.rio.transform()),
    )


def add_viewing_zenith_band(
    item: pystac.Item,
    viewing_zenith_band_label: str,
    viewing_zenith_band_da: xr.DataArray,
    tmp_folder: Path,
) -> Band:
    viewing_zenith_band_path = tmp_folder / f"{viewing_zenith_band_label}.tiff"
    if viewing_zenith_band_path.exists():
        viewing_zenith_band_da = rioxarray.open_rasterio(viewing_zenith_band_path)
    else:
        viewing_zenith_band_da.rio.to_raster(viewing_zenith_band_path)

    return add_asset(
        item=item,
        asset_path=viewing_zenith_band_path,
        asset_label=viewing_zenith_band_label,
        asset_description=viewing_zenith_band_label,
        asset_common_name=viewing_zenith_band_label,
        asset_nodata=0,
        asset_epsg=f"EPSG:{viewing_zenith_band_da.rio.crs.to_epsg()}",
        asset_geometry=item.geometry,
        asset_bbox=item.bbox,
        asset_shape=viewing_zenith_band_da.shape[-2:],
        asset_transform=list(viewing_zenith_band_da.rio.transform()),
    )


def add_mtd_tl(
    item: pystac.Item,
    mtd_tl_path: Path,
    target_da: xr.DataArray,
    tmp_folder: Path,
) -> list[Band]:
    tmp_folder = tmp_folder / "mtd_tl"
    tmp_folder_viewing_zenith = tmp_folder / "viewing_zenith"
    tmp_folder_viewing_azimuth = tmp_folder / "viewing_azimuth"
    tmp_folder_viewing_zenith.mkdir(exist_ok=True, parents=True)
    tmp_folder_viewing_azimuth.mkdir(exist_ok=True, parents=True)
    mtd_tl_ds = mtd_tl_to_dataset(mtd_tl_path=mtd_tl_path, target_da=target_da)

    view_azimuth_da = mtd_tl_ds["view_azimuth"].mean("detector")
    view_zenith_da = mtd_tl_ds["view_zenith"].mean("detector")
    return [
        add_viewing_azimuth_band(
            item=item,
            tmp_folder=tmp_folder_viewing_azimuth,
            viewing_azimuth_band_da=view_azimuth_da.sel(band=view_azimuth_band_label),
            viewing_azimuth_band_label=f"VIEW_AZIMUTH_{view_azimuth_band_label.item()}",
        )
        for view_azimuth_band_label in view_azimuth_da.band
    ] + [
        add_viewing_zenith_band(
            item=item,
            tmp_folder=tmp_folder_viewing_zenith,
            viewing_zenith_band_da=view_zenith_da.sel(band=view_zenith_band_label),
            viewing_zenith_band_label=f"VIEW_ZENITH_{view_zenith_band_label.item()}",
        )
        for view_zenith_band_label in view_zenith_da.band
    ]
