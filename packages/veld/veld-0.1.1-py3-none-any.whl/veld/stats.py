# -*- coding: utf-8 -*-

import math


class StreamedVariance:
    """Helper class to compute variance in a streaming fashion

    This is a memory efficient approach to compute the variance, by only
    keeping track of counts, means, and squared deviations. See for instance:
    https://gertjanvandenburg.com/blog/thompson_sampling/

    Parameters
    ----------
    population : bool
        Whether to compute the population variance or not (default: False).

    """

    def __init__(self, population: bool = False):
        self.population = population

        self._count = 0
        self._mean = 0.0
        self._sqdev = 0.0

    @property
    def variance(self) -> float:
        if self._count == 0:
            return float("nan")
        if self.population:
            return self._sqdev / self._count
        return self._sqdev / (self._count - 1)

    @property
    def stdev(self) -> float:
        """Return the standard deviation (square root of the variance)

        If `population = True`, this corresponds to the population standard
        deviation, otherwise it corresponds to the sample standard deviation.
        """
        return math.sqrt(self.variance)

    def update(self, value: float) -> None:
        count = self._count + 1
        mean = self._mean + 1 / (self._count + 1) * (value - self._mean)
        sqdev = (
            self._sqdev
            + value * value
            + self._count * self._mean * self._mean
            - count * mean * mean
        )

        self._count = count
        self._mean = mean
        self._sqdev = sqdev
