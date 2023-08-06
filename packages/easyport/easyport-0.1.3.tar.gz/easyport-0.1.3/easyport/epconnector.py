from time import sleep

from pyftdi.ftdi import Ftdi

import dill


class FtdiConnector:
    # Connect to the USB-Ftdi interface
    _count = 0

    def __init__(self, setup=True):
        self.vendor = 0x403
        self.product = 0xaf80
        FtdiConnector._count += 1
        self.id = FtdiConnector._count
        self.baudrate = 115200
        self.device = None
        self.is_setup = False
        if setup:
            self.setup()

    def set_baudrate(self, rate):
        self.check_connect(True)
        self.baudrate = rate

    def set_vendor(self, id):
        self.check_connect(True)
        self.vendor = id

    def set_product(self, id):
        self.check_connect(True)
        self.product = id

    def set_id(self, id):
        self.check_connect(True)
        self.id = id

    def setup(self):
        try:
            Ftdi.add_custom_product(self.vendor, self.product)
        except ValueError:
            # if product exists everything is fine
            pass
        self.device = Ftdi.create_from_url("ftdi://" + hex(self.vendor) + ":" + hex(self.product) + "/" + str(self.id))
        self.device.set_baudrate(self.baudrate)
        self.is_setup = True
        self.write_ftdi(b'setup0')
        sleep(0.01)
        tmp = self.read_ftdi()
        if len(tmp) > 1:
            raise ValueError("Unknown response of device: " + str(tmp))
        if len(tmp) == 0:
            print("Easyport already configured or error with Setup routine. Continuing...")
            return
        if tmp[0] != b'setup1':
            raise ValueError("Unknown response of device: " + str(tmp))

    def write_ftdi(self, data):
        self.check_connect(False)
        self.device.write_data(data + b'\r')

    def read_ftdi(self):
        self.check_connect(False)
        x = b'1'
        y = 0
        while x[-1] != b'\r':
            tmp = self.device.read_data(1024)
            y += 1
            if len(tmp) != 0:
                y = 0
            if y > 1:
                break
            x += tmp
        return x[1:].split(b'\r')[:-1]

    def check_connect(self, already):
        if already and self.is_setup:
            raise AlreadyConnectedException("No changes can be made to connection parameters after connection")
        if not already and not self.is_setup:
            raise NotConnectedException("You need an active connection to send or receive. Use setup()")


class BasicEasyport(FtdiConnector):
    buffer = []

    def __init__(self, filepath=None, setup=True):
        super().__init__(setup)
        self.buffer = []
        self.module = 1
        self.memory = {}
        self.set_filepath(filepath)
        if self.filepath != None:
            try:
                self.load()
            except FileNotFoundError:
                print("Could not find specified save-file")
        if(setup):
            x = self.write(b'DV')
            sleep(0.1)
            print("Setup comlete! Easyport version " + x[2:].decode('ascii'))
        self.flush()


    def set_filepath(self, filepath):
        if filepath is None:
            self.filepath = None
        if filepath[-4:] != '.pkl':
            raise ValueError("Configuration file must be .pkl")

        self.filepath = filepath

    def set_module(self, id):
        self.module = id

    def read(self, reversed=False):
        self.buffer.extend(super(BasicEasyport, self).read_ftdi())
        try:
            if reversed:
                return self.buffer.pop()
            return self.buffer.pop(0)
        except IndexError:
            return None

    def flush(self):
        self.buffer = []

    def write(self, data, receive=True):
        super(BasicEasyport, self).write_ftdi(data)
        if receive:
            sleep(0.01)
            return self.read(reversed=False)

    def send_from_memory(self, name, value=0, modify=2, check=True, intformat=True):
        if name not in self.memory:
            raise ValueError("No item named " + name)
        x = self.memory[name]
        self.flush()

        if modify != 2:
            m = modify
        else:
            m = x[3]
        if m == 1:
            m = True
        else:
            m = False
        self.flush()
        y = self.send(m, x[0], x[1], x[2], check, value)
        if not intformat:
            return y
        z = self.convert(y)
        if x[4] is None or z < 0:
            return z
        z=(z*10)/0x7fff
        return x[4](z)



    def send(self, modify=True, inout=1, bbw=0, addr=0, check=True, value=0):
        if modify:
            send = b'M'
            if inout != 2:
                raise ValueError("Only Outputs can be modified")
        else:
            send = b'D'
        # inout = 0: add nothing
        if inout == 1:
            # Input
            send += b'E'
        elif inout == 2:
            # Output
            send += b'A'
        elif inout == 3:
            # Ereigniszeitgeber
            send += b'T'
        elif inout == 4:
            # fast counter
            send += b'C'

        # bbw = 0: add nothing
        if bbw == 1:
            send += b'B'
        elif bbw == 2:
            send += b'W'

        if addr >= 0:
            tmp = hex(addr)[2:]
            if len(tmp) > 2 or (bbw == 2 and len(tmp) > 1):
                raise ValueError("addr must either be -1 or a hexadecimalnumber containing 2 digits")
            if len(tmp) == 0:
                tmp = "0"
            if len(tmp) == 1 and bbw != 2:
                tmp = "0" + tmp
            tmp2 = str(self.module) + "." + tmp[0]
            if bbw != 2:
                tmp2 += "." + tmp[1]
            send += tmp2.encode('ascii')

        if modify:
            send += b'='
            tmp = hex(value)[2:]
            if len(tmp) > 4 or value < 0:
                raise ValueError("value to modify fust be positive and not greater than 0xFFFF")
            send += tmp.upper().encode('ascii')

        tmp = self.write(send , check)
        if check:
            return self.check_output(send,tmp,modify,bbw)
        return tmp


    def check_output(self,input,out, modify,bbw):
        if out is None or (not modify and out[:out.find(b'=')] != input[1:out.find(b'=') + 1]) or (
                modify and ((bbw > 0 and out != input[1:]) or (bbw == 0 and out[:-1] != input[1:]))):
            print("Unexpected output of Easyport: " + str(out) + "\n Send it: " + str(input))
        elif not out is None and modify and bbw == 0:
            a = out.find(b'=')
            if len(out) > 1 and len(out) - a == 3 and out[-1] == out[-2]:
                out = out[:-1]
        return out
    def save(self):
        if self.filepath is None:
            raise FileNotFoundError("Please specify a filepath on init or with set_filepath()")
        with open(self.filepath, 'wb') as f:
            dill.dump(self.memory, f)

    def load(self):
        if self.filepath is None:
            raise FileNotFoundError("Please specify a filepath on init or with set_filepath()")
        with open(self.filepath, 'rb') as f:
            self.memory = dill.load(f)

    def set(self, name, inout=1, bbw=0, addr=0, modify=2, calc=None):
        self.memory[name] = (inout, bbw, addr, modify, calc)

    def delete(self, name):
        if name not in self.memory:
            raise ValueError("No item named " + name)
        del self.memory[name]

    def list(self):
        for x, y in self.memory.items():
            print(x + ":\tInput/Output(1/2):" + str(y[0]) + "\tBit(0),Byte(1),Word(2):" + str(y[1]) + "\tAddress:"
                  + hex(y[2]) + "\tdefaultModify:" + str(y[3]))

    def convert(self, x):
        try:
            z = x.index(b'=')
            if z + 1 < len(x):
                return int(x[z + 1:], base=16)
        except ValueError:
            return -1
        return -1


class AlreadyConnectedException(Exception):
    # After connection no change can be made to connection parameters
    pass


class NotConnectedException(Exception):
    # can not send/receive when not connected
    pass
