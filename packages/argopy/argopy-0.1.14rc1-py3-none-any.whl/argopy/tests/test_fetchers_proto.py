import pytest
import xarray
from argopy.data_fetchers.proto import ArgoDataFetcherProto


class Fetcher(ArgoDataFetcherProto):

    def to_xarray(self, *args, **kwargs):
        super(Fetcher, self).to_xarray(*args, **kwargs)

    def filter_data_mode(self, *args, **kwargs):
        super(Fetcher, self).filter_data_mode(*args, **kwargs)

    def filter_qc(self, *args, **kwargs):
        super(Fetcher, self).filter_qc(*args, **kwargs)

    def filter_researchmode(self, *args, **kwargs):
        super(Fetcher, self).filter_researchmode(*args, **kwargs)


def test_required_methods():
    f = Fetcher()
    with pytest.raises(NotImplementedError):
        f.to_xarray()

    with pytest.raises(NotImplementedError):
        f.filter_data_mode(xarray.Dataset, str)

    with pytest.raises(NotImplementedError):
        f.filter_qc(xarray.Dataset)

    with pytest.raises(NotImplementedError):
        f.filter_researchmode(xarray.Dataset)

def test_dashboard():

    f = Fetcher()
    f.WMO = [13857]
    f.CYC = None
    assert isinstance(f.dashboard(url_only=True), str)

    f = Fetcher()
    f.WMO = [13857]
    f.CYC = [90]
    assert isinstance(f.dashboard(url_only=True), str)

    with pytest.warns(UserWarning):
        f = Fetcher()
        f.WMO = [1901393, 6902746]
        f.CYC = None
        f.dashboard(url_only=True)
