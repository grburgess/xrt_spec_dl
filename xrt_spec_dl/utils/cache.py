from typing import Optional, Dict
from pathlib import Path

from astropy.table import Table
from astropy.io.ascii import QDP

from .config import xrt_spec_dl_config

lightcurve_cache: Dict[str, Dict[str, str]] = {}


cache_path = Path(xrt_spec_dl_config.cache_dir).expanduser()

if not cache_path.exists():

    cache_path.mkdir()


for f in cache_path.glob("*.qdp"):

    grb, data_type = f.stem.split("_")

    if grb in lightcurve_cache:

        lightcurve_cache[grb][data_type] = str(f)

    else:

        lightcurve_cache[grb] = {}

        lightcurve_cache[grb][data_type] = str(f)


def check_cache(obs_id: str) -> bool:

    return obs_id in lightcurve_cache


def get_file_from_cache(obs_id: str, data_type: str) -> Optional[Table]:

    if data_type not in lightcurve_cache[obs_id]:

        return None

    file_name: str = lightcurve_cache[obs_id][data_type]

    qdp = QDP(table_id=0, names = ["time", "rate", "bkg", "fracexp"])

    return qdp.read(str(cache_path / file_name))


def store_file_in_cache(table: Table, obs_id: str, data_type: str) -> None:



    file_name = f"{obs_id}_{data_type}.qdp"

    table.write(cache_path / file_name, format="ascii.qdp")

    # add to cache

    if not check_cache(obs_id):

        lightcurve_cache[obs_id] = {}

    lightcurve_cache[obs_id][data_type] = file_name
