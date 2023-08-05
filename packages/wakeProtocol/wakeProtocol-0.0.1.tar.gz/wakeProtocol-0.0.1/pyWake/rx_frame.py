import enum
from pyWake import escapesym
from pyWake.crc import crc

ADDRESS_BITMASK = 0x80

class mode(enum.Enum):
    NORMAL = 0
    ESC = 1

class rxState(enum.Enum):
    WAIT_FEND = 0
    WAIT_ADDR = 1
    WAIT_CMD = 2
    WAIT_LEN = 3
    WAIT_DATA = 4
    WAIT_CRC = 5


class rxFrame:
    def __init__(self) -> None:
        self.command = 0
        self.address = 0
        self.escMode = mode.NORMAL
        self.state = rxState.WAIT_FEND
        self.data = bytearray()
        self.dataLen = 0
        self.crc = crc()
        self.isReceived = False

    def __ReadyCheck(func):
        def wrapper(self):
            if self.isReceived == False:
                raise ValueError("Frame is not received")
            return func(self)
        return wrapper

    def reset(self) -> None:
        self.command = 0
        self.data = bytearray()
        self.crc.reset()
        self.isReceived = False

    def feedChar(self, char) -> bool:
        #If initial state
        if self.state == rxState.WAIT_FEND:
            self.reset()
            if char == escapesym.FEND:
                self.state = rxState.WAIT_ADDR
                self.crc.addByte(char)
            return True
        
        #Check for escape mode request
        if char == escapesym.FESC:
            self.escMode = mode.ESC
            return True
        
        #Reverse byte stuffing
        if self.escMode == mode.ESC:
            if char == escapesym.TFEND:
                char = escapesym.FEND
            elif char == escapesym.TFESC:
                char = escapesym.FESC
            else:
                raise ValueError("Incorrect byte in escape mode")
            self.escMode = mode.NORMAL
        
        #Decode according to state
        if self.state == rxState.WAIT_ADDR:
            
            if char & ADDRESS_BITMASK:
                #The char is address
                self.address = char & 0x7f
                self.state = rxState.WAIT_CMD
                self.crc.addByte(self.address)
            else:
                #The char is command
                self.command = char
                self.state = rxState.WAIT_LEN
                self.crc.addByte(self.command)
            return True
        
        elif self.state == rxState.WAIT_CMD:
            if char & ADDRESS_BITMASK:
                raise ValueError("Command has msb set")
            self.command = char
            self.crc.addByte(self.command)
            self.state = rxState.WAIT_LEN
            return True
        
        elif self.state == rxState.WAIT_LEN:
            self.dataLen = char
            self.crc.addByte(self.dataLen)
            if char == 0:
                self.state = rxState.WAIT_CRC
            else:
                self.state = rxState.WAIT_DATA
            return True

        elif self.state == rxState.WAIT_DATA:
            self.data.append(char)
            self.crc.addByte(char)
            if len(self.data) == self.dataLen:
                self.state = rxState.WAIT_CRC
            return True
        
        elif self.state == rxState.WAIT_CRC:
            if char != self.crc.get():
                raise ValueError("Invalid CRC")
            self.isReceived = True
            self.state = rxState.WAIT_FEND
            return False

    @__ReadyCheck    
    def getData(self) -> bytes:
        return bytes(self.data)
    
    @__ReadyCheck
    def getCommand(self) -> int:
        return self.command