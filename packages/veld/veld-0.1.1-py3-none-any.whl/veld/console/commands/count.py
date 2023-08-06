# -*- coding: utf-8 -*-

import math

from ._base import VeldCommand


class CountCommand(VeldCommand):
    def __init__(self):
        super().__init__(
            name="count",
            title="Count the number of values in the data stream",
        )

    def handle(self) -> int:
        counts = None
        for values in self.default_stream_processor:
            if counts is None:
                counts = [0] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                counts[i] += 1

        counts = [] if counts is None else counts
        print(self.args.separator.join(map(str, counts)))
        return 0
