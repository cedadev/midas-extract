import os
import pytest
from pathlib import Path

from midas_extract.testing import get_file_path
home = Path.home()


def test_get_file_path_success():
    pth = '/badc/ukmo-midas/metadata/SRCC/SRCC.DATA'
    cache_file = get_file_path(pth)

    epth = os.path.join(home.as_posix(), '.mini_ceda_archive/archive', pth.strip('/'))
    assert cache_file.as_posix() == epth


def test_get_file_path_bad_url_fail():
    pth = 'sdf/sdf/sdf/sf'

    with pytest.raises(Exception) as excinfo:
        get_file_path(pth) 
        assert '404' in str(excinfo)
