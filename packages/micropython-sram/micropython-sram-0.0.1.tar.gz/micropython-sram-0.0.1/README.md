# micropython-sram
SRAM/EERAM library for micropython

Primary used to work with 23LCV1024 (SPI SRAM with battery backup) memory which can be used as EEPROM/Flash but with unlimited number of writes. For applications where you need offten writes.


Simple code just use default sequenatial mode and allow to read/write whole SRAM memory, in case of 23LCV1024 it's full 128kB.

Nice2have TODO:
  - support also other chips (for example 47xx, 48xx) and protocols (like I2C)
  - IO Stream support
  - Page/Byte access modes (for example to prevent overwritting other data by buffer overflow)
  - Filesystem emulation (? - maybe if there will be IOStream, then someother lib could be used?)
  - Direct support to write other data types than buffer ? Like string, int

