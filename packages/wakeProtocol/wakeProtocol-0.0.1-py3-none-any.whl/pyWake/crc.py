class crc:
    def __init__(self, initial = 0xde) -> None:
        initial &= 0xff
        self.initial = initial
        self.crcVal = initial & 0xff
    
    def addByte(self, b) -> int:
        b &= 0xff
        for i in range(8):
            if (b ^ self.crcVal) & 0x01 != 0:
                self.crcVal = ((self.crcVal ^ 0x18) >> 1) | 0x80
            else:
                self.crcVal = (self.crcVal >> 1) & ~0x80
            b = b >> 1
        return self.crcVal
    
    def addMultiple(self, *vars: int | list) -> int:
        for var in vars:
            if type(var) is int:
                self.addByte(var)
            elif type(var) is list:
                for subvar in var:
                    if type(subvar) is not int:
                        TypeError("Incorrect type")  
                    self.addByte(subvar)
            else:
                raise TypeError("Incorrect type")
        return self.crcVal
    
    def reset(self):
        self.crcVal = self.initial
    
    def get(self) -> int:
        return self.crcVal