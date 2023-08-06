# -*- coding: utf-8 -*-
from contextlib import contextmanager


class Counter:
    def __init__(self, *args, **kwargs):
        pass

    def inc(self, *args, **kwargs):
        pass

    def labels(self, *args, **kwargs):
        return self


class Gauge:
    def __init__(self, *args, **kwargs):
        pass

    def inc(self, *args, **kwargs):
        pass

    def dec(self, *args, **kwargs):
        pass

    def set(self, *args, **kwargs):
        pass

    def labels(self, *args, **kwargs):
        return self


class Histogram:
    def __init__(self, *args, **kwargs):
        pass

    def observe(self, *args, **kwargs):
        pass

    def labels(self, *args, **kwargs):
        return self

    @contextmanager
    def time(self, *args, **kwargs):
        yield
