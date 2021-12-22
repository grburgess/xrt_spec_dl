import urllib
from typing import Optional

import matplotlib.pyplot as plt

from astropy.io.ascii import QDP
from astropy.table import Table

from xrt_spec_dl.utils.cache import check_cache

from .utils import xrt_spec_dl_config
from .utils.cache import check_cache, get_file_from_cache, store_file_in_cache


def check(line: str) -> Optional[str]:

    if "! pc data" in line.decode().lower():

        return "pc"

    elif "! pc upper limits" in line.decode().lower():

        return "skip"

    elif "! wt data" in line.decode().lower():

        return "wt"

    else:

        None


class XRTLightCurve:
    def __init__(self, obs_id: str) -> None:

        """
        Create an XRT light curve from the XRT
        website using the ID number of the GRB

        :param id:
        :type id:
        :returns:

        """

        not_found: bool = True

        if xrt_spec_dl_config.use_cache:

            if check_cache(obs_id):

                # the grb is in the cache

                self._wt_table = get_file_from_cache(obs_id, "wt")

                self._pc_table = get_file_from_cache(obs_id, "pc")

                not_found = False

        if not_found:

            names = ["time", "rate", "bkg", "fracexp"]

            tables = []

            url = (
                f"https://www.swift.ac.uk/xrt_curves/{obs_id}/curve2_incbad.qdp"
            )

            data = urllib.request.urlopen(url)
            for line in data:

                tmp = check(line)

                if tmp is not None:

                    tables.append(tmp)

            try:

                wt_idx = tables.index("wt")

                tmp = QDP(table_id=wt_idx, names=names)

                self._wt_table: Table = tmp.read(url)

            except ValueError:

                self._wt_table = None

            try:

                pc_idx = tables.index("pc")

                tmp = QDP(table_id=pc_idx, names=names)

                self._pc_table: Table = tmp.read(url)

            except ValueError:

                self._pc_table = None

            # now store in cache

            if xrt_spec_dl_config.use_cache:

                if self._wt_table is not None:

                    store_file_in_cache(self._wt_table, obs_id, "wt")

                if self._pc_table is not None:

                    store_file_in_cache(self._pc_table, obs_id, "pc")

    @property
    def pc_data(self) -> Table:
        return self._pc_table

    @property
    def wt_data(self) -> Table:
        return self._wt_table

    @staticmethod
    def _plot_data(
        ax: plt.Axes,
        data: Table,
        color: str,
        with_err: bool = False,
        label="",
        **kwargs,
    ) -> None:

        time_down = data["time"] + data["time_nerr"]

        time_up = data["time"] + data["time_perr"]

        ax.hlines(
            data["rate"], time_down, time_up, color=color, label=label, **kwargs
        )

        if with_err:

            rate_down = data["rate"] + data["rate_nerr"]

            rate_up = data["rate"] + data["rate_perr"]

            ax.vlines(data["time"], rate_down, rate_up, color=color, **kwargs)

    def plot(
        self,
        pc_mode: bool = True,
        wt_mode: bool = False,
        pc_color: str = "#33F0B4",
        wt_color: str = "#E233F0",
        with_err: bool = True,
        **kwargs,
    ) -> plt.Figure:

        fig, ax = plt.subplots()

        if pc_mode and self._pc_table is not None:

            self._plot_data(
                ax, self._pc_table, pc_color, with_err, label="PC", **kwargs
            )

        if wt_mode and self._wt_table is not None:

            self._plot_data(
                ax, self._wt_table, wt_color, with_err, label="WT", **kwargs
            )

        ax.set(xscale="log", yscale="log", ylabel="count rate", xlabel="time")

        ax.legend()

        return fig
