import pytest
from pathlib import Path

from xrt_spec_dl import XRTLightCurve, download_xrt_spectral_data


_obs_id = 1071993

_grb = "210905A"


def test_download():

    p = Path("_tmp")

    p.mkdir(exist_ok=True)

    download_xrt_spectral_data(
        obs_id=f"0{_obs_id}",
        name=f"GRB {_grb}",
        mode="PC",
        tstart=239,
        tstop=446,
        destination_dir=f"{p}")

    for f in p.glob("*"):

        if not f.is_dir():
            f.unlink()



    



def test_light_curve():

    xrt = XRTLightCurve(obs_id=f"0{_obs_id}")

    xrt.plot(with_err=True, wt_mode=True)

    xrt.plot(with_err=True, wt_mode=False)

    xrt.plot(with_err=False, pc_mode=False, wt_mode=True)

    xrt.pc_data

    xrt.wt_data
