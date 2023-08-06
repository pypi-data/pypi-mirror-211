import xarray as xr
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def preview_rgb(
    ds: xr.Dataset,
    min_percentile: float = 5.0,
    max_percentile: float = 95.0,
    maximal_length: int = 200,
) -> None:
    w, h = ds.shape[-2:]

    step, mod = divmod(w if w > h else h, maximal_length)
    step -= mod != 0

    img = (
        ds.loc[:, :, ::step, ::step]
        .sel(
            band=[
                "B04",
                "B03",
                "B02",
            ]
        )
        .median("time")
        .compute()
        / 10_000
    )
    min_quantile, max_quantile = min_percentile / 100, max_percentile / 100
    quantiles = img.quantile([min_quantile, max_quantile], dim=("x", "y"))
    quantiles["quantile"] = ["min", "max"]
    min_quantiles = quantiles.sel(quantile="min")
    max_quantiles = quantiles.sel(quantile="max")

    normalized_img = (img - min_quantiles) / (max_quantiles - min_quantiles)

    clipped_img = normalized_img.clip(min=0, max=1)
    clipped_img.plot.imshow()
    plt.gca().set_aspect(aspect="equal")
    plt.show()


def preview_aux_data(
    ds: xr.Dataset,
    maximal_length: int = 200,
) -> None:
    w, h = ds.shape[-2:]

    step, mod = divmod(w if w > h else h, maximal_length)
    step -= mod != 0

    img = (
        ds.loc[:, :, ::step, ::step]
        .sel(
            band=["msl", "tco3", "tcwv"],
        )
        .median("time")
        .compute()
    )

    fig, axes = plt.subplots(1, 3)
    for ax, band_name in zip(axes, img.band):
        im = img.sel(band=band_name).plot.imshow(ax=ax, add_colorbar=False)
        ax.set_aspect(aspect="equal")
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
    plt.show()


def preview(
    ds: xr.Dataset,
    maximal_length: int = 200,
) -> None:
    if set(["B02", "B03", "B04"]).issubset(set(ds.band.values)):
        preview_rgb(ds, maximal_length=maximal_length)
    elif set(["msl", "tco3", "tcwv"]).issubset(set(ds.band.values)):
        preview_aux_data(ds, maximal_length=maximal_length)
