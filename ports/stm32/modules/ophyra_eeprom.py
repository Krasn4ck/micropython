import pyb
import time
from pyb import I2C
class M24C32_init(object):
    def __init__(self):
        self.addr = 80
        self.i2cm = I2C(1, I2C.MASTER)
        self.i2cm.init(I2C.MASTER, baudrate=400000)
class M24C32(M24C32_init):
    def write(eeaddress, value):
        data = bytearray(3)
        data[0] = eeaddress >> 8 #MSB
        data[1] = eeaddress & 0xFF #LSB
        data[2] = value
        self.i2c.send(data, self.addr)
        time.sleep(.05)
    def read(eeaddress):
        data = bytearray(2)
        data[0] = eeaddress >> 8 #MSB
        data[1] = eeaddress & 0xFF #LSB
        self.i2c.send(data,self.addr)
        value = self.i2c.recv(1,self.addr)
        return value[0]