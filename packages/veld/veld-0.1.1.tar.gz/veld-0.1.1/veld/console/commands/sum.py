# -*- coding: utf-8 -*-

import math

from typing import List
from typing import Optional

from ._base import VeldCommand


class SumCommand(VeldCommand):
    def __init__(self):
        super().__init__(
            name="sum",
            title="Sum the values in the data stream",
        )

    def handle(self) -> int:
        totals = None  # type: Optional[List[float]]
        for values in self.default_stream_processor:
            if totals is None:
                totals = [0] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                totals[i] += val

        totals = [] if totals is None else totals
        print(self.args.separator.join(map(str, totals)))
        return 0
