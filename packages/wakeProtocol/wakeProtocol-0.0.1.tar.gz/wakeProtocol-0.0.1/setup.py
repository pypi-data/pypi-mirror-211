from setuptools import setup, find_packages

VERSION= '0.0.1'
DESCRIPITON = 'Point binary protocol (above pySerial)'
LONG_DESCRIPTION = '''Wake - simple and lightweight binary protocol for exchange data
                        between PC and different devices. Protocol has address and
                        command fields, up to 255 bytes if data in one frame and
                        CRC-8 check.'''

setup(
    name='wakeProtocol',
    version=VERSION,
    author='N1X (Uladzimir Kisel)',
    author_email='nixblr@gmail.com',
    description=DESCRIPITON,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['pyserial', 'uart', 'rs-232', 'rs-485', 'p2p', 'serial', 'Wake'],
    url='https://github.com/Nixblr/pyWake',
    classifiers=['Programming Language :: Python :: 3']
)