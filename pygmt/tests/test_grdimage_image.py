"""
Test Figure.grdimage on 3-band RGB images.
"""

import pytest
from pygmt import Figure
from pygmt.datasets import load_blue_marble

rioxarray = pytest.importorskip("rioxarray")


@pytest.fixture(scope="module", name="xr_image")
def fixture_xr_image():
    """
    Load the image data from Blue Marble as an xarray.DataArray with shape {"band": 3,
    "y": 180, "x": 360}.
    """
    xr_image = load_blue_marble(resolution="01d")
    assert xr_image.sizes == {"band": 3, "y": 180, "x": 360}
    return xr_image


@pytest.mark.mpl_image_compare
def test_grdimage_image():
    """
    Plot a 3-band RGB image using file input.
    """
    fig = Figure()
    fig.grdimage(grid="@earth_day_01d")
    return fig


@pytest.mark.benchmark
@pytest.mark.mpl_image_compare(filename="test_grdimage_image.png")
def test_grdimage_image_dataarray(xr_image):
    """
    Plot a 3-band RGB image using xarray.DataArray input.
    """
    fig = Figure()
    fig.grdimage(grid=xr_image)
    return fig


