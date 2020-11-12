from machine import Pin
from micropython import const
from time import sleep_ms

TM1638_DSP_ON = const(0x08)
TM1638_CMD3 = const(0x80)
TM1638_CMD1 = const(0x40)
TM1638_CMD2 = const(0xc0)
TM1638_READ = const(0x02)
_SEGMENTS = bytearray(
    b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')


class TM1638(object):
    """
    TM1638
    """

    def __init__(self, stb, clk, dio, brt=7):
        self.stb = stb
        self.clk = clk
        self.dio = dio
        self._brightness = brt
        self._on = TM1638_DSP_ON
        self.DIO = Pin(self.dio, Pin.OUT, value=0)
        self.CLK = Pin(self.clk, Pin.OUT, value=1)
        self.STB = Pin(self.stb, Pin.OUT, value=1)
        self.clear()
        self._write_dsp_vtrl()

    def clear(self):
        """
        write 0x00 to all address
        """
        self._write_data_command()
        self.STB.value(0)
        self._set_address(0x00)
        for i in range(16):
            self._byte(0x00)
        self.STB.value(1)

    def _write_dsp_vtrl(self):
        """
        docstring
        """
        self._command(TM1638_CMD3 | self._on | self._brightness)

    def _byte(self, b):
        """
        send byte data 
        """
        for i in range(8):
            self.CLK.value(0)
            self.DIO.value((b >> i) & 1)
            self.CLK.value(1)

    def _command(self, cmd):
        """
        docstring
        """
        self.STB.off()
        self._byte(cmd)
        self.STB.on()

    def _write_data_command(self):
        """
        docstring
        """
        self._command(TM1638_CMD1)

    def _set_address(self, addr=0x00):
        """
        docstring
        """
        self._byte(TM1638_CMD2 | addr)

    def _scan_keys(self):
        """
        docstring
        """
        pressed = 0
        self.DIO = Pin(self.dio, Pin.IN, Pin.PULL_UP)
        for i in range(8):
            self.CLK.value(0)
            if self.DIO.value():
                pressed |= 1 << i
            self.CLK.value(1)
        self.DIO = Pin(self.dio, Pin.OUT, value=0)
        return pressed

    def write(self, data, pos=0):
        """
        docstring
        """
        self._write_data_command()
        self.STB.value(0)
        self._set_address(pos)
        for b in data:
            self._byte(b)
        self.STB.value(1)

    def led(self, pos, val):
        """
        docstring
        """
        self.write([val], (pos << 1) + 1)

    def brightness(self, val):
        """
        docstring
        """
        self._brightness = val
        self._write_dsp_vtrl()

    def leds(self, val):
        """
        docstring
        """
        pass

    def segment(self, segments, pos=0):
        """
        pass
        """
        self._write_data_command()
        for seg in segments:
            self.STB.off()
            self._set_address(pos << 1)
            self._byte(seg)
            pos += 1
            self.STB.on()

    def keys(self):
        """
        return a byte representing which key is pressed, LSB is SW1
        """
        key = 0
        self.STB.off()
        self._byte(TM1638_CMD1 | TM1638_READ)
        for i in range(4):
            key |= self._scan_keys() << i
        self.STB.on()
        return key

    def encode_digit(self, digit):
        """
        docstring
        """
        return _SEGMENTS[digit & 0x0f]

    def encode_char(self, char):
        """
        docstring
        """
        o = ord(char)
        if o == 32:
            return _SEGMENTS[36]  # space
        if o == 42:
            return _SEGMENTS[38]  # star/degrees
        if o == 45:
            return _SEGMENTS[37]  # dash
        if o >= 65 and o <= 90:
            return _SEGMENTS[o-55]  # uppercase A-Z
        if o >= 97 and o <= 122:
            return _SEGMENTS[o-87]  # lowercase a-z
        if o >= 48 and o <= 57:
            return _SEGMENTS[o-48]  # 0-9

    def encode_string(self, string):
        """
        docstring
        """
        segments = bytearray(len(string.replace('.', '')))
        j = 0
        for i in range(len(string)):
            if string[i] == '.' and j > 0:
                segments[j-1] |= (1 << 7)
                continue
            segments[j] = self.encode_char(string[i])
            j += 1
        return segments

    def display_number(self, num):
        """Display a numeric value -9999999 through 99999999, right aligned."""
        # limit to range -9999999 to 99999999
        num = max(-9999999, min(num, 99999999))
        string = '{0: >8d}'.format(num)
        self.segment(self.encode_string(string))

    def show(self, string, pos=0):
        """Displays a string"""
        segments = self.encode_string(string)
        self.segment(segments[:8], pos)

    def display_hex(self, val):
        """
        docstring
        """
        string = '{:08x}'.format(val & 0xffffffff)
        self.segment(self.encode_string(string))


if __name__ == "__main__":
    a = TM1638(0, 4, 5, 8)
    a.led(7, 1)
    a.brightness(3)
    a.display_hex(0x8efc)
    # a.display_number(8888888)
