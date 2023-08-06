# -*- coding: utf-8 -*-

from typing import List
from typing import Optional

from ._base import VeldCommand


class CumSumCommand(VeldCommand):
    def __init__(self):
        super().__init__(
            name="cumsum",
            title="Compute the cumulative sum of the input stream",
        )

    def register(self):
        super().register()

    def handle(self) -> int:
        out_values = None  # type: Optional[List[float]]
        for values in self.default_stream_processor:
            if out_values is None:
                out_values = [0] * len(values)

            for i in range(len(values)):
                out_values[i] += values[i]
            print(self.args.separator.join(map(str, out_values)))
        return 0
