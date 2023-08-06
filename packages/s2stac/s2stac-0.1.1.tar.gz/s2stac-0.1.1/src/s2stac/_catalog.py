import shutil
from tempfile import TemporaryDirectory
import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pathlib import Path
import rioxarray

from datetime import datetime, timezone
from shapely.geometry import Polygon, mapping
from ._aux_data import add_ecmwf

from ._img_data import add_img_data_bands
from ._mtd_tl import add_mtd_tl
from ._qi_data import add_qi_data


class __TmpFolderPersistence:
    def __init__(self):
        self.tmp_folders = []

    def add_tmp_folder(
        self,
    ) -> Path:
        tmp_folder = TemporaryDirectory()
        self.tmp_folders.append(tmp_folder)
        return Path(tmp_folder.name)

    def __del__(self):
        for tmp_folder in self.tmp_folders:
            tmp_folder.cleanup()


__tmp_folder_persistence = __TmpFolderPersistence()


def safe_folder_to_item(
    safe_folder: Path,
    catalog_folder: Path,
    include_img_data: bool = True,
    include_aux_data: bool = True,
    include_qi_data: bool = True,
    include_footprint: bool = True,
    include_cloud_proba: bool = True,
    include_ecmwf: bool = True,
    include_mtd_tl: bool = True,
) -> pystac.Item:
    target_da_10m = rioxarray.open_rasterio(
        list(safe_folder.glob("GRANULE/*/IMG_DATA/*10*/*B02*"))[0]
    )
    target_da_20m = rioxarray.open_rasterio(
        list(safe_folder.glob("GRANULE/*/IMG_DATA/*20*/*B02*"))[0]
    )
    target_da_60m = rioxarray.open_rasterio(
        list(safe_folder.glob("GRANULE/*/IMG_DATA/*60*/*B02*"))[0]
    )

    catalog_folder = catalog_folder / safe_folder.stem
    catalog_folder.mkdir(exist_ok=True)

    bbox = target_da_10m.rio.bounds()
    xmin, ymin, xmax, ymax = bbox
    footprint = mapping(
        Polygon(
            [
                [xmin, ymin],
                [xmin, ymax],
                [xmax, ymax],
                [xmax, ymin],
            ]
        )
    )
    datetime_utc = datetime.now(tz=timezone.utc)

    # Item definition
    item_id = safe_folder.stem
    item = pystac.Item(
        id=item_id,
        geometry=footprint,
        bbox=bbox,
        datetime=datetime_utc,
        properties={},
    )

    item.common_metadata.platform = "MSI"
    item.common_metadata.instruments = ["Sentinel-2"]
    item.common_metadata.gsd = 10

    # Add EO data
    eo_extension = EOExtension.ext(item, add_if_missing=True)

    bands = []
    # Write MSK_DETFOO data
    if include_img_data:
        bands += add_img_data_bands(
            item=item,
            img_data_folder=list(safe_folder.glob("GRANULE/*/IMG_DATA/"))[0],
            tmp_folder=catalog_folder,
        )
    if include_qi_data:
        bands += add_qi_data(
            item=item,
            qi_folder=list(safe_folder.glob("GRANULE/*/QI_DATA/"))[0],
            target_da_10m=target_da_10m,
            target_da_20m=target_da_20m,
            target_da_60m=target_da_60m,
            tmp_folder=catalog_folder,
            include_footprint=include_footprint,
            include_cloud_proba=include_cloud_proba,
        )
    if include_aux_data:
        bands += add_ecmwf(
            item=item,
            ecmwft_path=list(safe_folder.glob("GRANULE/*/AUX_DATA/AUX_ECMWFT"))[0],
            target_da=target_da_10m,
            tmp_folder=catalog_folder,
        )
    if include_mtd_tl:
        bands += add_mtd_tl(
            item=item,
            mtd_tl_path=list(safe_folder.glob("GRANULE/*/MTD_TL.xml"))[0],
            target_da=target_da_10m,
            tmp_folder=catalog_folder,
        )

    eo_extension.apply(
        bands=bands,
    )

    # Add Projection
    projection_extension = ProjectionExtension.ext(item, add_if_missing=True)
    projection_extension.apply(
        epsg=target_da_10m.rio.crs.to_epsg(),
        transform=list(target_da_10m.rio.transform()),
        shape=target_da_10m.shape[-2:],
        bbox=bbox,
    )

    return item


def create_stac_catalog(
    safe_folders: list[Path],
    catalog_folder: Path | None = None,
    overwrite_catalog_folder: bool = False,
    include_img_data: bool = True,
    include_qi_data: bool = True,
    include_aux_data: bool = True,
    include_footprint: bool = True,
    include_cloud_proba: bool = True,
    include_ecmwf: bool = True,
    include_mtd_tl: bool = True,
) -> pystac.Catalog:
    if catalog_folder is None:
        catalog_folder = __tmp_folder_persistence.add_tmp_folder()
    elif overwrite_catalog_folder:
        shutil.rmtree(path=str(catalog_folder))
    catalog_folder.mkdir(exist_ok=True, parents=True)

    catalog = pystac.Catalog(id="s2-catalog", description="Sentinel-2 STAC")

    for safe_folder in safe_folders:
        catalog.add_item(
            safe_folder_to_item(
                safe_folder=safe_folder,
                catalog_folder=catalog_folder,
                include_img_data=include_img_data,
                include_aux_data=include_aux_data,
                include_qi_data=include_qi_data,
                include_footprint=include_footprint,
                include_cloud_proba=include_cloud_proba,
                include_ecmwf=include_ecmwf,
                include_mtd_tl=include_mtd_tl,
            )
        )

    catalog.normalize_hrefs(str(catalog_folder))
    catalog.save(catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED)

    return catalog
