# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class ZsdFrame(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.tag = self._io.read_bytes(3)
        if not self.tag == b"\x56\x44\x46":
            raise kaitaistruct.ValidationNotEqualError(b"\x56\x44\x46", self.tag, self._io, u"/seq/0")
        self.new_size = self._io.read_u1()
        self.time_raw = self._io.read_s8le()
        self.dist = self._io.read_s4le()
        self.wheel1_value = self._io.read_bits_int_le(12)
        self.wheel1_weight = self._io.read_bits_int_le(4)
        self.wheel2_value = self._io.read_bits_int_le(12)
        self.wheel2_weight = self._io.read_bits_int_le(4)
        self._io.align_to_byte()
        self.index = self._io.read_u4le()
        self.angle = self._io.read_u1()
        self.flags = self._io.read_u1()
        self.dist_ext = self._io.read_u1()
        if self.new_size != 48:
            self.slope = self._io.read_u1()

        if self.new_size == 48:
            self.old_size = self._io.read_u1()

        _on = self.frame_size
        if _on == 60:
            self._raw_data = self._io.read_bytes(self.frame_size)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = ZsdFrame.Sensors(6, _io__raw_data, self, self._root)
        elif _on == 84:
            self._raw_data = self._io.read_bytes(self.frame_size)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = ZsdFrame.Sensors(4, _io__raw_data, self, self._root)
        elif _on == 112:
            self._raw_data = self._io.read_bytes(self.frame_size)
            _io__raw_data = KaitaiStream(BytesIO(self._raw_data))
            self.data = ZsdFrame.Sensors(4, _io__raw_data, self, self._root)
        else:
            self.data = self._io.read_bytes(self.frame_size)
        self.crc32 = self._io.read_u4le()

    class Channels(KaitaiStruct):
        def __init__(self, channel_count, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.channel_count = channel_count
            self._read()

        def _read(self):
            self.status = self._io.read_u1()
            self.channel = [None] * (self.channel_count)
            for i in range(self.channel_count):
                self.channel[i] = self._io.read_bits_int_le(12)



    class FourByteArray(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            i = 0
            while not self._io.is_eof():
                self.data.append(self._io.read_u4le())
                i += 1



    class Sensors(KaitaiStruct):
        def __init__(self, channel_count, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.channel_count = channel_count
            self._read()

        def _read(self):
            self.sensor = []
            i = 0
            while not self._io.is_eof():
                self.sensor.append(ZsdFrame.Channels(self.channel_count, self._io, self, self._root))
                i += 1



    class ScanFlag(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved = self._io.read_bits_int_be(1) != 0
            self.by_path2 = self._io.read_bits_int_be(1) != 0
            self.by_path1 = self._io.read_bits_int_be(1) != 0
            self.by_time = self._io.read_bits_int_be(1) != 0
            self.ready = self._io.read_bits_int_be(1) != 0
            self.error = self._io.read_bits_int_be(1) != 0
            self.o2_done = self._io.read_bits_int_be(1) != 0
            self.o1_done = self._io.read_bits_int_be(1) != 0


    class SensorFlag(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.lost = self._io.read_bits_int_be(1) != 0
            self.crc = self._io.read_bits_int_be(1) != 0
            self.hdr = self._io.read_bits_int_be(1) != 0
            self.uart = self._io.read_bits_int_be(1) != 0
            self.res3 = self._io.read_bits_int_be(1) != 0
            self.res2 = self._io.read_bits_int_be(1) != 0
            self.res1 = self._io.read_bits_int_be(1) != 0
            self.low = self._io.read_bits_int_be(1) != 0


    @property
    def frame_size(self):
        if hasattr(self, '_m_frame_size'):
            return self._m_frame_size if hasattr(self, '_m_frame_size') else None

        self._m_frame_size = (self.new_size if self.new_size != 48 else self.old_size)
        return self._m_frame_size if hasattr(self, '_m_frame_size') else None

    @property
    def raw(self):
        if hasattr(self, '_m_raw'):
            return self._m_raw if hasattr(self, '_m_raw') else None

        _pos = self._io.pos()
        self._io.seek(0)
        self._m_raw = self._io.read_bytes((self.frame_size + 28))
        self._io.seek(_pos)
        return self._m_raw if hasattr(self, '_m_raw') else None

    @property
    def dist_sum(self):
        if hasattr(self, '_m_dist_sum'):
            return self._m_dist_sum if hasattr(self, '_m_dist_sum') else None

        self._m_dist_sum = (self.dist + (self.dist_ext << 31))
        return self._m_dist_sum if hasattr(self, '_m_dist_sum') else None

    @property
    def time(self):
        if hasattr(self, '_m_time'):
            return self._m_time if hasattr(self, '_m_time') else None

        self._m_time = (self.time_raw if self.time_raw > 0 else 0)
        return self._m_time if hasattr(self, '_m_time') else None

    @property
    def old_format(self):
        if hasattr(self, '_m_old_format'):
            return self._m_old_format if hasattr(self, '_m_old_format') else None

        self._m_old_format = self.new_size == 48
        return self._m_old_format if hasattr(self, '_m_old_format') else None


