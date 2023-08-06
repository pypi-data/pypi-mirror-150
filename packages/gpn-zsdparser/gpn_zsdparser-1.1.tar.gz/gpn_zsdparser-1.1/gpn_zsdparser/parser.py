import csv
import logging
from binascii import crc32
from collections import namedtuple
from io import BufferedReader
from typing import List
from uuid import UUID

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    create_engine,
    Integer,
    LargeBinary,
    SmallInteger,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .zsd_frame import ZsdFrame


_frame_header_size = 32
# arbitrary number
_sql_transaction_size = 100000
# must be bigger than max magnetogram frame size in bytes
_zsd_initial_read = 1024

_MagnetogramParameters = namedtuple(
    "MagnetogramParameters",
    ["frame_size", "has_slope", "old_format", "sensor_count", "channel_count"],
)

_logger = logging.getLogger(__name__)


def zsd_to_csv(input_obj: BufferedReader, output_obj: BufferedReader):
    """
    Parse given .zsd file to text, in CSV format.

    Parameters:
        input_obj: BufferedReader
            input .zsd file object
        output_obj: BufferedReader
            output CSV file object
    """

    params = _magnetogram_parameters(
        ZsdFrame.from_bytes(input_obj.peek(_zsd_initial_read))
    )
    writer = csv.writer(output_obj)

    writer.writerow(
        _csv_header(params.sensor_count, params.channel_count, params.has_slope)
    )

    while frame_raw := input_obj.read(_frame_header_size + params.frame_size):
        frame = ZsdFrame.from_bytes(frame_raw)
        row = [
            "VDF",
            frame.frame_size,
            frame.time_raw,
            frame.dist,
            frame.wheel1_value,
            frame.wheel1_weight,
            frame.wheel2_value,
            frame.wheel2_weight,
            frame.index,
            frame.angle,
            format(frame.flags, "x"),
            frame.dist_ext,
            frame.dist_sum,
        ]
        if params.has_slope:
            row.append(frame.slope)
        for sensor in frame.data.sensor:
            row.append(format(sensor.status, "x"))
            row += sensor.channel
        row.append(format(frame.crc32, "x"))
        checksum = (
            _vid260_checksum(frame.raw) if params.old_format else crc32(frame.raw)
        )
        row.append(frame.crc32 == checksum)
        writer.writerow(row)


def zsd_to_mem(input_obj: BufferedReader) -> List[ZsdFrame]:
    """
    Parse given .zsd file to list.

    Parameters:
        input_obj: BufferedReader
            .zsd file object
    Returns:
        List[ZsdFrame]: parsed frames
    """

    params = _magnetogram_parameters(
        ZsdFrame.from_bytes(input_obj.peek(_zsd_initial_read))
    )
    frames = []
    while frame_raw := input_obj.read(_frame_header_size + params.frame_size):
        frames.append(ZsdFrame.from_bytes(frame_raw))
    return frames


def zsd_to_sql(
    input_obj: BufferedReader,
    db_connection: str,
    magnetogram_id: str,
    transaction_size: int = _sql_transaction_size,
):
    """
    Parse given .zsd file, write to SQL database.

    Parameters:
        input_obj: BufferedReader
            .zsd file object
        db_connection: str
            SQLAlchemy connection string to database
        magnetogram_id: str
            UUID of current magnetogram (string representation)
            Any input understandable by uuid.UUID works, actually
        transaction_size: int
            number of frames inserted in one SQL transaction
    """

    params = _magnetogram_parameters(
        ZsdFrame.from_bytes(input_obj.peek(_zsd_initial_read))
    )

    session_maker = sessionmaker(
        bind=create_engine(db_connection)
    )

    session = session_maker()
    uniq_frame_ids = set()
    transaction_count = 0

    while frame_raw := input_obj.read(_frame_header_size + params.frame_size):
        sql_frame = _sql_frame(ZsdFrame.from_bytes(frame_raw), UUID(magnetogram_id), params)

        if sql_frame.index in uniq_frame_ids:
            _logger.warning(f'Duplicate frame index with id = {sql_frame.index}')
            continue

        session.add(sql_frame)
        uniq_frame_ids.add(sql_frame.index)
        transaction_count += 1

        if transaction_count >= transaction_size:
            transaction_count = 0
            session.commit()

    session.commit()


def _csv_header(sensor_count: int, channel_count: int, has_slope: bool) -> List[str]:
    """
    Generate correct header for CSV file
    """
    header = [
        "Tag",
        "Size",
        "Time",
        "Dist",
        "Wheel1_value",
        "Wheel1_weight",
        "Wheel2_value",
        "Wheel2_weight",
        "Index",
        "Angle",
        "Flags",
        "Dist_ext",
        "Dist_sum",
    ]
    if has_slope:
        header.append("Slope")

    for i in range(1, sensor_count + 1):
        header.append(f"Status {i}")
        header += [f"{i}.{j}" for j in range(1, channel_count + 1)]

    header.append("CRC")
    header.append("CRCOK")

    return header


def _magnetogram_parameters(init_frame: ZsdFrame) -> _MagnetogramParameters:
    """
    Determine magnetogram parameters from magnetogram frame
    """
    parameters = _MagnetogramParameters(
        frame_size=init_frame.frame_size,
        has_slope=hasattr(init_frame, "slope"),
        old_format=init_frame.old_format,
        sensor_count=len(init_frame.data.sensor),
        channel_count=init_frame.data.channel_count,
    )
    return parameters


def _vid260_checksum(data: bytes) -> int:
    """
    Calculates checksum as per VID 2.60 specification.
    """
    word_length = 4  # calculated over 4-byte words, refer to VID 2.60 spec
    checksum = 0
    for i in range(0, len(data) // word_length):
        checksum += int.from_bytes(
            data[i * word_length : (i + 1) * word_length], "little"
        )
    return checksum % (1 << word_length * 8)


class _MagnetogramContent(declarative_base()):
    __tablename__ = "content"

    magnetogram_id = Column(PG_UUID(as_uuid=True), primary_key=True)
    index = Column(Integer, primary_key=True, autoincrement=False)
    time = Column(BigInteger, nullable=False)
    dist = Column(BigInteger, nullable=False, index=True)
    wheel1_v = Column(SmallInteger, nullable=False)
    wheel2_v = Column(SmallInteger, nullable=False)
    angle = Column(SmallInteger, nullable=False)
    flags = Column(ARRAY(Boolean), nullable=False)
    slope = Column(SmallInteger, nullable=True)
    sensor_value = Column(LargeBinary, nullable=False)
    sensor_status = Column(LargeBinary, nullable=False)
    crc_ok = Column(Boolean, nullable=False)


def _sql_frame(
    frame: ZsdFrame, magnetogram_id: UUID, parameters: _MagnetogramParameters
) -> _MagnetogramContent:
    """
    Creates frame ready to SQL insert from generated Kaitai frame
    """
    return _MagnetogramContent(
        magnetogram_id=magnetogram_id,
        index=frame.index,
        time=frame.time,
        dist=frame.dist_sum,
        wheel1_v=frame.wheel1_value,
        wheel2_v=frame.wheel2_value,
        angle=frame.angle,
        flags=_get_flags(frame.flags),
        slope=frame.slope if parameters.has_slope else None,
        crc_ok=True,
        sensor_value=_encode_nums(
            [i for _ in [sensor.channel for sensor in frame.data.sensor] for i in _]
        ),
        sensor_status=_encode_nums(
            [i.status for i in frame.data.sensor], byte_length=1
        ),
    )


def _get_flags(flags: int) -> List[bool]:
    """
    Creates list of boolean values corresponding to truth value
    of individual bits in 8-bit integer
    """
    flag_list = []
    for i in range(0, 8):
        flag_list.insert(0, bool((flags >> i) & 1))
    return flag_list


def _encode_nums(numbers: List[int], byte_length: int = 2) -> bytes:
    """
    Encodes list of numbers to bytearray
    """
    serialized = b""
    for number in numbers:
        serialized += number.to_bytes(length=byte_length, byteorder="little")
    return serialized
