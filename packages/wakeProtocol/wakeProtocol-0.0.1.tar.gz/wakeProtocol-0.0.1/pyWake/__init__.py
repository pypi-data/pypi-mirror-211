import enum
#############################################################
#						Wake frame format                   #
#   | FEND | ADDR | CMD | LEN | Data0 | … | DataN | CRC |   #
#############################################################

__version__ = '0.1.0'

class escapesym(enum.IntEnum):
    FEND = 0xc0     #Frame END
    FESC = 0xDB     #Frame Escape
    TFEND = 0xDC    #Transponded Frame End
    TFESC = 0xDD    #Transponded Frame Escape

class std_command(enum.IntEnum):
    NOP = 0
    ERROR = 1
    ECHO = 2
    INFO = 3
    SET_ADDRESS = 4
    GET_ADDRESS = 5