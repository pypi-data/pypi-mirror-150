# -*- coding: utf-8 -*-

import sys

from wilderness import Application
from wilderness import Command

from veld.__version__ import __version__

from .commands.barcount import BarCountCommand
from .commands.comparison import EqualCommand
from .commands.comparison import GreaterEqualCommand
from .commands.comparison import GreaterThanCommand
from .commands.comparison import LessEqualCommand
from .commands.comparison import LessThanCommand
from .commands.comparison import NotEqualCommand
from .commands.count import CountCommand
from .commands.cumsum import CumSumCommand
from .commands.histogram import HistogramCommand
from .commands.log import LogCommand
from .commands.max import MaxCommand
from .commands.mean import MeanCommand
from .commands.median import MedianCommand
from .commands.min import MinCommand
from .commands.mode import ModeCommand
from .commands.quantile import QuantileCommand
from .commands.scatter import ScatterPlotCommand
from .commands.stdev import StandardDeviationCommand
from .commands.sum import SumCommand
from .commands.variance import VarianceCommand


class VeldApplication(Application):
    def __init__(self):
        super().__init__(
            "veld",
            version=__version__,
            title="easy command line statistics",
            author="Gerrit J.J. van den Burg",
        )

    def register(self):
        self.add_argument(
            "-V",
            "--version",
            help="show version information and exit",
            action="version",
            version=__version__,
        )
        self.add_argument(
            "--debug",
            help="Enable debug mode",
            action="store_true",
            description=(
                "Debug mode disables the default exception handling, which "
                "can be useful for debugging."
            ),
        )

    def set_excepthook(self) -> None:
        sys_hook = sys.excepthook

        def exception_handler(exception_type, value, traceback):
            if self.args.debug:
                sys_hook(exception_type, value, traceback)
            else:
                print(value, file=sys.stderr)

        sys.excepthook = exception_handler

    def run_command(self, command: Command) -> int:
        self.set_excepthook()
        return super().run_command(command)


def build_application() -> Application:
    app = VeldApplication()
    app.set_prolog(
        "Below are the available Veld commands. Use veld help <command>\n"
        "to learn more about each command."
    )
    app.set_epilog(
        "For more information about Veld, visit:\n"
        "https://github.com/GjjvdBurg/Veld"
    )

    group = app.add_group("univariate statistics")
    group.add(SumCommand())
    group.add(MeanCommand())
    group.add(ModeCommand())
    group.add(MedianCommand())
    group.add(StandardDeviationCommand())
    group.add(VarianceCommand())
    group.add(QuantileCommand())

    group = app.add_group("extreme values and counts")
    group.add(MinCommand())
    group.add(MaxCommand())
    group.add(CountCommand())

    group = app.add_group("filtering values")
    group.add(LessThanCommand())
    group.add(LessEqualCommand())
    group.add(GreaterThanCommand())
    group.add(GreaterEqualCommand())
    group.add(EqualCommand())
    group.add(NotEqualCommand())

    group = app.add_group("math operators")
    group.add(LogCommand())
    group.add(CumSumCommand())

    # group = app.add_group("hypothesis testing")
    # group.add(PairedTTestCommand())

    group = app.add_group("plotting")
    # group.add(LinePlotCommand())
    group.add(ScatterPlotCommand())
    group.add(HistogramCommand())
    group.add(BarCountCommand())
    return app
