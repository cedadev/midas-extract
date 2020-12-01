"""Testing and tutorial utilities module."""
# Most of this code copied and adapted from xarray
from pathlib import Path
import hashlib
import subprocess as sp

from urllib.request import urlretrieve


_default_cache_dir = Path.home() / ".mini_ceda_archive"


def file_md5_checksum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        hash_md5.update(f.read())

    return hash_md5.hexdigest()


# idea copied from xarray that borrowed it from Seaborn
def get_file_path(
    name,
    cache: bool = True,
    cache_dir: Path = _default_cache_dir,
    github_url: str = "https://github.com/cedadev/mini-ceda-archive",
    sub_dir: str = "archive",
    branch: str = "main",
):
    """
    Get local path to a file from an online repository (requires internet).

    If a local copy is found then always use that to avoid network traffic.

    Parameters
    ----------
    name : str
        Name of the file containing the dataset. If no suffix is given, assumed
        to be netCDF ('.nc' is appended). The name may contain
    cache_dir : Path
        The directory in which to search for and write cached data.
    cache : bool
        If True, then cache data locally for use on subsequent calls
    github_url : str
        Github repository where the data is stored
    sub_dir: str
        Sub-directory in github repo
    branch : str
        The git branch to download from


    Return
    ------

    A file path (string).
    """
    name = Path(name.lstrip('/'))
    cache_dir = cache_dir.absolute()
    fullname = sub_dir / name

    local_file = cache_dir / fullname
    md5name = Path(fullname.as_posix() + ".md5")
    md5file = cache_dir / md5name

    if not local_file.is_file():

        # This will always leave this directory on disk.
        # We may want to add an option to remove it.
        local_file.parent.mkdir(parents=True, exist_ok=True)

        url = "/".join((github_url, "raw", branch, fullname.as_posix()))
        print(f'Retrieving: {url}')
        urlretrieve(url, local_file)

        url = "/".join((github_url, "raw", branch, md5name.as_posix()))
        print(f'Retrieving: {url}')
        urlretrieve(url, md5file)

        localmd5 = file_md5_checksum(local_file)

        with open(md5file) as f:
            remotemd5 = f.read().strip().split()[0]

        if localmd5 != remotemd5:
            local_file.unlink()
            msg = """
            MD5 checksum does not match, try downloading dataset again.
            """
            raise OSError(msg)

    return local_file 

