"""
Tests for fitcircle.
"""

import os

import numpy as np
import pandas as pd
import numpy.testing as npt
import pytest
from pygmt import fitcircle
from pygmt.exceptions import GMTInvalidInput
from pygmt.helpers import GMTTempFile
from pygmt.src import which


@pytest.fixture(scope="module", name="data")
def fixture_data():
    """
    Load the sample data from the sat_03 remote file.
    """
    fname = which("@sat_03.txt", download="c")
    data = pd.read_csv(
        fname,
        header=None,
        skiprows=1,
        sep="\t",
        names=["longitutde", "latitude", "z"],
    )
    return data


def test_fitcircle_no_outfile(data):
    """
    Test fitcircle with no set outfile.
    """
    result = fitcircle(data=data, normalize=True)
    assert result.shape == (7, 3)
    # Test longitude results
    npt.assert_allclose(result.iloc[:,0].min(), 52.7434273422)
    npt.assert_allclose(result.iloc[:,0].max(), 330.243649573)
    npt.assert_allclose(result.iloc[:,0].mean(), 223.078116476)
    npt.assert_allclose(result.iloc[:,0].median(), 232.7449849)
    # Test latitude results
    npt.assert_allclose(result.iloc[:,1].min(), -21.2085369093)
    npt.assert_allclose(result.iloc[:,1].max(), 21.2085369093)
    npt.assert_allclose(result.iloc[:,1].mean(), -7.8863683297)
    npt.assert_allclose(result.iloc[:,1].median(), -18.406777)

def test_fitcircle_file_output(data):
    """
    Test that fitcircle returns a file output when it is specified.
    """
    with GMTTempFile(suffix=".txt") as tmpfile:
        result = fitcircle(
            data=data, normalize=True, outfile=tmpfile.name, output_type="file"
        )
        assert result is None  # return value is None
        assert os.path.exists(path=tmpfile.name)  # check that outfile exists