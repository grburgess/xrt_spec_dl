import urllib3
from pathlib import Path
import os
import time
import requests
import tarfile

from .utils.logging import setup_logger
from .utils.file_utils import (
    sanitize_filename,
    if_directory_not_existing_then_make,
)

log = setup_logger(__name__)


_allow_modes = ("BOTH", "PC", "WT")


def download_xrt_spectral_data(
    obs_id: str,
    name: str,
    tstart: float,
    tstop: float,
    mode: str = "BOTH",
    filename: str = "xrt.tar.gz",
    destination_dir: str = ".",
):

    """TODO describe function

    :param obs_id:
    :type obs_id: str
    :param name:
    :type name: str
    :param tstart:
    :type tstart: float
    :param tstop:
    :type tstop: float
    :param mode:
    :type mode: str
    :param filename:
    :type filename: str
    :param destination_dir:
    :type destination_dir: str
    :returns:

    """
    if mode not in _allow_modes:

        log.error(f"{mode} is not one of {','.join(_allow_modes)}")

        raise RuntimeError()

    # set the time slice to analyze
    timeslices: str = f"{tstart}-{tstop}"

    destination: Path = sanitize_filename(destination_dir)

    if_directory_not_existing_then_make(destination)

    # build the form
    data = dict(
        targ=obs_id,
        name=name,
        pubpriv=1,
        public=1,
        z=0,
        sno=0,
        name1="a",
        time1=timeslices,
        mode1=mode,
        name2="",
        time2="",
        mode2=mode,
        name3="",
        time3="",
        mode3=mode,
        name4="",
        time4="",
        mode4=mode,
        grade0="0",
    )

    log.info("requesting build...")

    r = requests.post(
        "http://www.swift.ac.uk/xrt_spectra/build_slice_spec.php", params=data
    )

    url = r.url

    r2 = r
    itr = 0

    if "Error" in r2.content.decode():

        print(r2.content.decode())

        raise RuntimeError()

    while "This page will be reloaded in 30 seconds" in r2.content.decode():

        log.info("sleeping 30 seconds ...")

        time.sleep(30)

        if itr == 0:
            log.info(f"requesting {url} ...")

        r2 = requests.get(url)

        itr += 1

    log.info(f"downloading: {os.path.join(url, filename)}")
    connection_pool = urllib3.PoolManager()
    resp = connection_pool.request("GET", os.path.join(url, "a.tar.gz"))
    ""

    final_path: Path = destination / filename

    with final_path.open("wb") as f:
        f.write(resp.data)

    resp.release_conn()

    tar = tarfile.open(final_path)

    tar.extractall(path=destination)

    paths = dict()

    pc = (
        dict(
            source=os.path.join(destination_dir, "apcsource.pi"),
            bak=os.path.join(destination_dir, "apcbak.pi"),
            rmf=os.path.join(destination_dir, "apc.rmf"),
            arf=os.path.join(destination_dir, "apc.arf"),
        ),
    )

    wt = dict(
        source=os.path.join(destination_dir, "awtsource.pi"),
        bak=os.path.join(destination_dir, "awtbak.pi"),
        rmf=os.path.join(destination_dir, "awt.rmf"),
        arf=os.path.join(destination_dir, "awt.arf"),
    )

    if mode == "BOTH":

        paths["PC"] = pc
        paths["WT"] = wt

    elif mode == "PC":

        paths["PC"] = pc

    else:

        paths["WT"] = wt

    return paths
