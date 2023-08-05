import serial
import struct
from pyWake.rx_frame import rxFrame
from pyWake.crc import crc
from pyWake import escapesym

class Wake:
    def __init__(self, portName = 'COM1', baudrate = 115200) -> None:
        self.timeout = 0
        self.address = 0
        self.command = 0
        self.portName = portName
        self.baudrate = baudrate
        self.port = serial.Serial(self.portName, self.baudrate)
        self.data = list()
        self.crc = crc()
        self.port.timeout = 1.0

    def open(self):
        if (self.port.is_open):
            return
        self.port.name = self.portName
        self.port.port = self.baudrate
        self.port.open()

    def close(self):
        self.port.close

    def io(self) -> rxFrame:
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()
        self.port.write(self.__assembly())
        rx = rxFrame()
        rb = self.port.read()
        if len(rb) != 1:
            raise TimeoutError("Rx timeout")
        while rx.feedChar(rb[0]):
            rb = self.port.read()
            if len(rb) != 1:
                raise TimeoutError("Rx timeout")
        return rx


    def __bytestuffing(self, input: bytes) -> bytes:
        output = bytearray()
        for b in input:
            if b == escapesym.FEND:
                output.extend((escapesym.FESC, escapesym.TFEND))
            elif b == escapesym.FESC:
                output.extend((escapesym.FESC, escapesym.TFESC))
            else:
                output.append(b)
        return bytes(output)

    def __assembly(self) -> bytes:
        self.crc.reset()
        self.crc.addByte(escapesym.FEND)
        if (self.address != 0):
            self.crc.addByte(self.address)
        self.crc.addMultiple(self.command, len(self.data), self.data)
        result = bytearray()
        if (self.address != 0):
            result.append(self.address | 0x80)
        result.append(self.command)
        result.append(len(self.data))
        result.extend(self.data)
        result.append(self.crc.get())
        stuffed = self.__bytestuffing(bytes(result))
        result = bytearray()
        result.append(escapesym.FEND)
        result.extend(stuffed)
        return bytes(result)

    def setAddress(self, address) -> None:
        if address < 0:
            raise ValueError("Address can't be negative!")
        if address > 127:
            raise ValueError("Address can't be > 127!")
        self.address = address
    
    def setCommand(self, command) -> None:
        if command < 0:
            raise ValueError("Command can't be negative!")
        if command > 127:
            raise ValueError("Address can't be > 127!")
        self.command = command & 0xff

    def addByte(self, b: int):
        if type(b) != int:
            raise TypeError('Argument must be an integer.')
        b &= 0xff
        self.data.append(b)

    def addInt32(self, b: int):
        if type(b) != int:
            raise TypeError('Argument must be an integer.')
        b &= 0xffff
        tmp = struct.pack('<H', b)
        self.data.append(tmp)

    def addString(self, s: str):
        pass

    def clearData(self):
        self.data.clear()