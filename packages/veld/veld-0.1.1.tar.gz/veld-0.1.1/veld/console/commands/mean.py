# -*- coding: utf-8 -*-

import math

from typing import List
from typing import Optional

from ._base import VeldCommand


class MeanCommand(VeldCommand):
    def __init__(self):
        super().__init__(
            name="mean",
            title="Find the mean (average) of the values in the data stream",
        )

    def handle(self) -> int:
        counts = []  # type: List[int]
        sums = None  # type: Optional[List[float]]
        for values in self.default_stream_processor:
            if sums is None:
                sums = [0] * len(values)
                counts = [0] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                sums[i] += values[i]
                counts[i] += 1

        safediv = lambda a, b: float("nan") if b == 0 else a / b

        sums = [] if sums is None else sums
        means = [safediv(s, c) for s, c in zip(sums, counts)]
        print(self.args.separator.join(map(str, means)))
        return 0
