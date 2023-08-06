# Low level driver for SPI Serial SRAM 23LCV1024
# Copyright (c) 2022 Petr Kracik

from sram import SRAM

class SRAM23LCV1024(SRAM):
    INSTRUCTION_READ = 0x03
    INSTRUCTION_WRITE = 0x02
    INSTRUCTION_RDMR = 0x05
    INSTRUCTION_WRMR = 0x01

    def __init__(self, spi, cs):
        super().__init__()
        self._size = 131072  # 0x00000 - 0x1FFFF
        self._spi = spi
        self._cs = cs


    @property
    def mode(self):
        tmp = bytearray(1)
        tmp[0] = self.INSTRUCTION_RDMR

        self._cs.value(0)
        self._spi.write(tmp)
        data = self._spi.read(1)
        self._cs.value(1)

        return ord(data)


    @mode.setter
    def mode(self, value):
        tmp = bytearray(2)
        tmp[0] = self.INSTRUCTION_WRMR
        tmp[1] = chr(value)

        self._cs.value(0)
        self._spi.write(tmp)
        self._cs.value(1)

        return value == self.mode


    def read(self, address, count):
        if address > self.size - 1 or address < 0:
            raise ValueError("Attemped to read outside of address range (0--{})".format(self.size - 1))

        tmp = bytearray(4)
        tmp[0] = self.INSTRUCTION_READ
        tmp[1] = ( address >> 16 ) & 0xFF
        tmp[2] = ( address >> 8 ) & 0xFF
        tmp[3] = ( address ) & 0xFF

        self._cs.value(0)
        self._spi.write(tmp)
        data = self._spi.read(count)
        self._cs.value(1)

        return data


    def write(self, address, data, check=True):
        if address > self.size - 1 or address < 0:
            raise ValueError("Attemped to write outside of address range (0--{})".format(self.size - 1))

        tmp = bytearray(4)
        tmp[0] = self.INSTRUCTION_WRITE
        tmp[1] = ( address >> 16 ) & 0xFF
        tmp[2] = ( address >> 8 ) & 0xFF
        tmp[3] = ( address ) & 0xFF

        self._cs.value(0)
        self._spi.write(tmp)
        self._spi.write(data)
        self._cs.value(1)

        if check:
            check = self.read(len(data), address)
            return check == data
        else:
            return True
