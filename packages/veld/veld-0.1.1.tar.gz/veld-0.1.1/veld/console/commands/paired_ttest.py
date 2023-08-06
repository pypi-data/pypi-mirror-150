# -*- coding: utf-8 -*-

from typing import List

from ._base import VeldCommand


class PairedTTestCommand(VeldCommand):
    def __init__(self):
        super().__init__(
            name="paired_ttest",
            title="Perform a paired t-test on a two-dimensional input stream",
            description="TODO",
        )

    def register(self) -> None:
        super().register()
        self.add_argument(
            "--nan",
            help="How to handle NaN values",
            choices=["raise", "propagate", "omit"],
            description="TODO",
            default="omit",
        )
        self.add_argument(
            "--alternative",
            help="The alternative of the hypothesis test",
            choices=["two-sided", "less", "greater"],
            default="two-sided",
            description="TODO",
        )

    def handle(self) -> int:
        differences = [] # type: List[float]
        raise NotImplementedError

