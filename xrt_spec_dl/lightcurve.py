import matplotlib.pyplot as plt

from astropy.io.ascii import QDP
from astropy.table import Table


class XRTLightCurve:
    def __init__(self, obs_id: str) -> None:

        """
        Create an XRT light curve from the XRT
        website using the ID number of the GRB

        :param id:
        :type id:
        :returns:

        """
        names = ["time", "rate", "bkg", "fracexp"]

        tmp = QDP(table_id=0, names=names)

        self._wt_table: Table = tmp.read(
            f"https://www.swift.ac.uk/xrt_curves/{obs_id}/curve2_incbad.qdp"
        )

        tmp = QDP(table_id=1, names=names)

        self._pc_table: Table = tmp.read(
            f"https://www.swift.ac.uk/xrt_curves/{obs_id}/curve2_incbad.qdp"
        )

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

        if pc_mode:

            self._plot_data(
                ax, self._pc_table, pc_color, with_err, label="PC", **kwargs
            )

        if wt_mode:

            self._plot_data(
                ax, self._wt_table, wt_color, with_err, label="WT", **kwargs
            )

        ax.set(xscale="log", yscale="log", ylabel="count rate", xlabel="time")

        ax.legend()

        return fig
