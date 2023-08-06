# -*- coding: utf-8 -*-

from ._plot import VeldPlotCommand


class ScatterPlotCommand(VeldPlotCommand):
    def __init__(self) -> None:
        super().__init__(
            name="scatter",
            title="Show a scatterplot of two-dimensional data",
        )

    def register(self) -> None:
        super().register()
        self.add_argument(
            "-t",
            "--transpose",
            help="Transpose the data before plotting",
            action="store_true",
        )

    def handle(self) -> int:
        all_values = self._consume_stream()
        if all_values is None:
            return 1

        if self.args.transpose:
            all_values = list(map(list, zip(*all_values)))

        if not len(all_values) == 2:
            raise ValueError("Can only plot two-dimensional data")

        self.plt.scatter(all_values[0], all_values[1])
        self.set_plot_attributes()
        self.plt.show()
        return 0
