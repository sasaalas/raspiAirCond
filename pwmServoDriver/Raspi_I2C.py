#!/usr/bin/python

from smbus2 import SMBus
import syslog
import sys

# ===========================================================================
# Raspi_I2C Base Class
# ===========================================================================

class Raspi_I2C :

  def __init__(self, address, bus=SMBus(1), debug=False):
    self.address = address
    self.bus = bus
    self.debug = debug

  def reverseByteOrder(self, data):
    "Reverses the byte order of an int (16-bit) or long (32-bit) value"
    # Courtesy Vishal Sapre
    dstr = hex(data)[2:].replace('L','')
    byteCount = len(dstr[::2])
    val = 0
    for i, n in enumerate(range(byteCount)):
      d = data & 0xFF
      val |= (d << (8 * (byteCount - i - 1)))
      data >>= 8
    return val

  def write8(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    try:
      self.bus.write_byte_data(self.address, reg, value)              
    except IOError:
      syslog.syslog(syslog.LOG_ERR, "I2C: Error accessing register. Check your I2C address")
      return -1

  def writeList(self, reg, list):
    "Writes an array of bytes using I2C format"
    try:      
      self.bus.write_i2c_block_data(self.address, reg, list)
    except IOError:
      syslog.syslog(syslog.LOG_ERR, "I2C: Error accessing register. Check your I2C address")
      return -1

  def readList(self, reg, length):
    "Read a list of bytes from the I2C device"
    results = []
    try:
      results = self.bus.read_i2c_block_data(self.address, reg, length)      
      return results
    except IOError:
      syslog.syslog(syslog.LOG_ERR, "I2C: Error accessing register. Check your I2C address")
      return -1

  def readU8(self, reg):
    "Read an unsigned byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)      
      return result
    except IOError:
      syslog.syslog(syslog.LOG_ERR, "I2C: Error accessing register. Check your I2C address")
      return -1

  def readS8(self, reg):
    "Reads a signed byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)      
      if (result > 127):
        return result - 256
      else:
        return result
    except IOError:
      syslog.syslog(syslog.LOG_ERR, "I2C: Error accessing register. Check your I2C address")
      return -1

  def readU16(self, reg):
    "Reads an unsigned 16-bit value from the I2C device"
    try:
      hibyte = self.bus.read_byte_data(self.address, reg)
      result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg+1)      
      return result
    except IOError:
      syslog.syslog(syslog.LOG_ERR, "I2C: Error accessing register. Check your I2C address")
      return -1

  def readS16(self, reg):
    "Reads a signed 16-bit value from the I2C device"
    try:
      hibyte = self.bus.read_byte_data(self.address, reg)
      if (hibyte > 127):
        hibyte -= 256
      result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg+1)      
      return result
    except IOError:
      syslog.syslog(syslog.LOG_ERR, "I2C: Error accessing register. Check your I2C address")
      return -1 
