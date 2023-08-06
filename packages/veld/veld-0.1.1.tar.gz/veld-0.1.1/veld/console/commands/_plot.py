# -*- coding: utf-8 -*-

import importlib

from types import ModuleType

from ._base import VeldCommand


class VeldPlotCommand(VeldCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._plt = None

    @property
    def plt(self) -> ModuleType:
        # This is here for lazy evaluation, as it is only needed for the
        # plotting commands and otherwise slows down all veld commands.
        if self._plt is None:
            self._plt = importlib.import_module("matplotlib.pyplot")
        return self._plt

    def register(self) -> None:
        super().register()
        group = self.add_argument_group(title="plot options")
        group.add_argument(
            "--xmin", help="Lower limit of the horizontal axis", type=float
        )
        group.add_argument(
            "--xmax", help="Upper limit of the horizontal axis", type=float
        )
        group.add_argument(
            "--ymin", help="Lower limit of the vertical axis", type=float
        )
        group.add_argument(
            "--ymax", help="Upper limit of the vertical axis", type=float
        )
        group.add_argument(
            "--xlabel", help="Axis label for the horizontal axis"
        )
        group.add_argument(
            "--ylabel",
            help="Axis label for the vertical axis",
        )
        group.add_argument("--title", help="Title for the plot")

    def set_plot_attributes(self) -> None:
        # Set common plot options
        self.plt.xlim(left=self.args.xmin, right=self.args.xmax)
        self.plt.ylim(bottom=self.args.ymin, top=self.args.ymax)
        if self.args.xlabel is not None:
            self.plt.xlabel(self.args.xlabel)
        if self.args.ylabel is not None:
            self.plt.ylabel(self.args.ylabel)
        if self.args.title:
            self.plt.title(self.args.title)
