# -*- coding: utf-8 -*-

import math

from typing import List
from typing import Optional

from ._base import VeldCommand


class MaxCommand(VeldCommand):
    def __init__(self):
        super().__init__(
            name="max",
            title="Find the maximum of the values in the data stream",
        )

    def handle(self) -> int:
        maxs = None  # type: Optional[List[float]]
        for values in self.default_stream_processor:
            if maxs is None:
                maxs = [-float("inf")] * len(values)

            for i in range(len(values)):
                val = values[i]
                if math.isnan(val):
                    continue
                maxs[i] = max(maxs[i], val)

        maxs = [] if maxs is None else maxs
        print(self.args.separator.join(map(str, maxs)))
        return 0
