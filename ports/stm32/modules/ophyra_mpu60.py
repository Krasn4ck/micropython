import pyb
import time
from pyb import I2C
class MPU6050_init(object):
    def __init__(self):
        self.saddres = 104
        self.accel = 0
        self.env_gyr = 0
        self.env_accel = 0
        self.gyr = 0
        self.acel = 2
        self.tem = 340
        self.g = 0
        self.y = 128
        self.sen = 0
        self.i2c = I2C(1, I2C.MASTER)
        self.i2c.init(I2C.MASTER, baudrate=400000)

class MPU6050(MPU6050_init):
    def init(self,accel, gyr):
        if accel == 2:
            self.env_accel = 0
            self.g = 16384
        elif accel == 4:
            self.env_accel = 8
            self.g = 8192
        elif accel == 8:
            self.env_accel = 16
            self.g = 4096
        else:
            self.env_accel = 24
            self.g = 2048
        if gyr == 250: 
            self.env_gyr = 0
            self.sen = 131
        elif gyr == 500:
            self.env_gyr = 8
            self.sen = 65.5
        elif gyr == 1000:
            self.env_gyr = 16
            self.sen = 32.8
        else:
            self.env_gyr = 24
            self.sen = 16.4
        self.i2c.mem_write(0, self.saddres, 107)
        self.i2c.mem_write(self.env_accel, self.saddres, 28)
        self.i2c.mem_write(self.env_gyr, self.saddres, 28)
    def accX(self):
        x=self.i2c.mem_read(2,self.saddres,59)
        x=int.from_bytes(x,'big')
        if x > 32767:
            x = (65536 - x)*-1
            return x/self.g
        else:
            return x/self.g
    def accY(self):
		x=self.i2c.mem_read(2,self.saddres,61)
		x=int.from_bytes(x,'big')
		if x > 32767:
			x = (65536 - x)*-1
			return x/self.g
		else:
			return x/self.g
    def accZ(self):
		x=self.i2c.mem_read(2,self.saddres,63)
		x=int.from_bytes(x,'big')
		if x > 32767:
			x = (65536 - x)*-1
			return x/self.g
		else:
			return x/self.g
    def temp(self):
		x = ord(self.i2c.mem_read(1,self.saddres,65))
		x1 = ord(self.i2c.mem_read(1,self.saddres,66))
		z2 = x << 8
		x3 = z2 + x1
		value = x3 / self.tem
		value2 = value + 36.53
		value3 = value2 / 10
		return value3
    def gyrX(self):
        x=self.i2c.mem_read(2,self.saddres,67)
        x=int.from_bytes(x,'big')
        if x > 32767:
            x = (65536 - x)*-1
            return x/self.sen
        else:
            return x/self.sen
    def gyrY(self):
        x=self.i2c.mem_read(2,self.saddres,69)
        x=int.from_bytes(x,'big')
        if x > 32767:
            x = (65536 - x)*-1
            return x/self.sen
        else:
            return x/self.sen
    def gyrZ(self):
		x=self.i2c.mem_read(2, self.saddres, 71)
		x=int.from_bytes(x,'big')
		if x > 32767:
			x = (65536 - x)*-1
			return x/self.sen
		else:
			return x/self.sen
    def write(self,num,addres):
        self.i2c.mem_write(num,self.saddres,addres)
    def read(self,addres):
		x=ord(self.i2c.mem_read(1,self.saddres,addres))
		return x