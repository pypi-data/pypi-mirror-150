# -*- coding: utf-8 -*-

import enum

from typing import Callable

from ._base import VeldCommand


class ComparisonOperator(enum.Enum):
    lt = "less than"
    le = "less than or equal to"
    eq = "equal to"
    gt = "greater than"
    ge = "greater than or equal to"
    ne = "not equal to"


COMMAND_TITLES = {
    "lt": "Keep only inputs that are less than a given threshold",
    "le": "Keep only inputs that are less than or equal to a given threshold",
    "eq": "Keep only inputs that equal a given value",
    "gt": "Keep only inputs that are greater than a given threshold",
    "ge": "Keep only inputs that are greater than or equal to a given threshold",
    "ne": "Keep only inputs that are not equal to a given value",
}


class _ComparisonCommand(VeldCommand):
    def __init__(self, op: ComparisonOperator):
        self._op = op
        super().__init__(name=op.name, title=COMMAND_TITLES[op.name])

    @property
    def _operator(self) -> Callable[[float, float], bool]:
        if self._op == ComparisonOperator.lt:
            return lambda x, y: x < y
        elif self._op == ComparisonOperator.le:
            return lambda x, y: x <= y
        elif self._op == ComparisonOperator.eq:
            return lambda x, y: x == y
        elif self._op == ComparisonOperator.gt:
            return lambda x, y: x > y
        elif self._op == ComparisonOperator.ge:
            return lambda x, y: x >= y
        elif self._op == ComparisonOperator.ne:
            return lambda x, y: x != y
        raise ValueError(f"Unknown operator: {self._op}")

    def register(self):
        super().register()
        self.add_argument(
            "testvalue", help="Value to test against", type=float
        )
        self.add_argument(
            "--all",
            action="store_true",
            help="For multidimensional input, keep rows where all values match",
            description=(
                "For multidimensional input the default behavior is to keep "
                "those rows where any value matches. With this option only "
                "the rows are kept where _all_ values match the filter."
            ),
        )

    def handle(self) -> int:
        func = lambda x: self._operator(x, self.args.testvalue)
        sep = self.args.separator

        for values in self.default_stream_processor:
            if len(values) == 1 and func(values[0]):
                print(values[0])
            else:
                matches = [func(val) for val in values]
                if self.args.all:
                    if all(matches):
                        print(sep.join(map(str, values)))
                else:
                    if any(matches):
                        print(sep.join(map(str, values)))
        return 0


class LessThanCommand(_ComparisonCommand):
    def __init__(self):
        super().__init__(ComparisonOperator.lt)


class LessEqualCommand(_ComparisonCommand):
    def __init__(self):
        super().__init__(ComparisonOperator.le)


class EqualCommand(_ComparisonCommand):
    def __init__(self):
        super().__init__(ComparisonOperator.eq)


class GreaterThanCommand(_ComparisonCommand):
    def __init__(self):
        super().__init__(ComparisonOperator.gt)


class GreaterEqualCommand(_ComparisonCommand):
    def __init__(self):
        super().__init__(ComparisonOperator.ge)


class NotEqualCommand(_ComparisonCommand):
    def __init__(self):
        super().__init__(ComparisonOperator.ne)
