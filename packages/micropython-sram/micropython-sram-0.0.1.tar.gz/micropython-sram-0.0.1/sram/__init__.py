# Base driver for SRAM
# Copyright (c) 2022 Petr Kracik

__version__ = "0.0.1"
__license__ = "MIT"
__author__ = "Petr Kracik"


class SRAM:
    def __init__(self):
        self._size = 0


    @property
    def size(self):
        return self._size


    def read(self):
        return self.read(0, 1)


    def read(self, address, count):
        raise NotImplementedError()


    def write(self, data):
        return self.write(0, data)


    def write(self, address, data, check=True):
        raise NotImplementedError()

