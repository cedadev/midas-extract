import os
import shutil
import pytest
from pathlib import Path

from midas_extract.testing import get_file_path
home = Path.home()
mini_ceda_archive = os.path.join(home.as_posix(), '.mini_ceda_archive')


def setup_module():
    "Destroy the local copy of the mini ceda archive repo."
    if os.path.isdir(mini_ceda_archive) and mini_ceda_archive.endswith('.mini_ceda_archive'):
        shutil.rmtree(mini_ceda_archive)


# Run this twice to check it downloads and then checks local file
@pytest.mark.parametrize('dummy', [1, 2])
def test_get_file_path_success(dummy):
    pth = '/badc/ukmo-midas/metadata/SRCC/SRCC.DATA'
    cache_file = get_file_path(pth)

    epth = os.path.join(home.as_posix(), '.mini_ceda_archive/archive', pth.strip('/'))
    assert cache_file.as_posix() == epth


def test_get_file_path_bad_url_fail():
    pth = 'sdf/sdf/sdf/sf'

    with pytest.raises(Exception) as excinfo:
        get_file_path(pth) 
        assert '404' in str(excinfo)
