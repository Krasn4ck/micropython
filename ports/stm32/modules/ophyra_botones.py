from machine import Pin
class sw_in(object):
    def __init__(self):
        self.p1 = Pin('PC2',Pin.IN,Pin.PULL_UP)
        self.p2 = Pin('PD5',Pin.IN,Pin.PULL_UP)
        self.p3 = Pin('PD4',Pin.IN,Pin.PULL_UP)
        self.p4 = Pin('PD3',Pin.IN,Pin.PULL_UP)
class sw(sw_in):
    def sw1(self):
        return self.p1.value()
    def sw2(self):
        return self.p2.value()        
    def sw3(self):
        return self.p3.value() 	
    def sw4(self):
        return self.p4.value()