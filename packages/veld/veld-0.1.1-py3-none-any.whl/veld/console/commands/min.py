# -*- coding: utf-8 -*-

import math

from typing import List
from typing import Optional

from ._base import VeldCommand


class MinCommand(VeldCommand):
    def __init__(self):
        super().__init__(
            name="min",
            title="Find the minimum of the values in the data stream",
        )

    def register(self):
        super().register()

    def handle(self) -> int:
        mins = None  # type: Optional[List[float]]
        for values in self.default_stream_processor:
            if mins is None:
                mins = [float("inf")] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                mins[i] = min(mins[i], val)

        mins = [] if mins is None else mins
        print(self.args.separator.join(map(str, mins)))
        return 0
