"""
COS-03 MultiGas sensor frame parser and channel mapper.

Parses 64-byte HID record frames from the vendor protocol and maps
channel readings to the frontend greenhouse data structure.

Frame layout (63-64 bytes):
  [0:3]   Header: 0xAA 0x26 0x24
  [3]     Channel number (1-based)
  [4]     Record type / flags
  [5:9]   Measurement value — big-endian IEEE 754 float.
          If non-zero, this IS the reading.
          If zero, the reading is encoded as a raw integer at [38:40]
          (big-endian uint16), scaled by /10 when the unit contains "%".
  [9:14]  Metadata (timestamp / sequence bytes)
  [14:?]  Unit string (UTF-8, null-terminated, within a fixed window)
  [21:?]  Channel name (UTF-8, null-terminated, within a fixed window)
  [62:63] CRC / checksum (last 2 bytes)
"""
import struct
import time

# ── Channel → frontend field mapping ────────────────────────────────
# Keys match the fields returned by get_greenhouse_data() in sensor_data.py.
_CHANNEL_MAP = {
    1: {"name": "土壤湿度",   "unit": "%",   "field": "soilMoisture"},
    2: {"name": "土壤温度",   "unit": "℃",  "field": "airTemp"},
    3: {"name": "空气湿度",   "unit": "%",   "field": "airHumidity"},
    4: {"name": "pH",         "unit": "",    "field": "ph"},
    5: {"name": "氮",         "unit": "mg/kg", "field": "nitrogen"},
    6: {"name": "磷",         "unit": "mg/kg", "field": "phosphorus"},
    7: {"name": "钾",         "unit": "mg/kg", "field": "potassium"},
    8: {"name": "叶片湿度",   "unit": "%",   "field": "airHumidity"},
    9: {"name": "光照强度",   "unit": "lux", "field": "light"},
    10: {"name": "CO₂浓度",   "unit": "ppm", "field": "co2"},
    11: {"name": "EC电导率",  "unit": "mS/cm", "field": "ec"},
}


def _extract_utf8(frame: bytes, start: int, window: int = 24) -> str:
    """Extract a null-terminated UTF-8 string from *frame* starting at *start*."""
    raw = frame[start : start + window]
    end = raw.find(0x00)
    if end == -1:
        end = len(raw)
    try:
        return raw[:end].decode("utf-8")
    except UnicodeDecodeError:
        return ""


def _extract_ascii(frame: bytes, start: int, window: int = 7) -> str:
    """Extract a null-terminated ASCII string from *frame* starting at *start*."""
    raw = frame[start : start + window]
    end = raw.find(0x00)
    if end == -1:
        end = len(raw)
    try:
        return raw[:end].decode("ascii")
    except UnicodeDecodeError:
        return ""


def parse_store_frame(frame: bytes) -> dict:
    """
    Parse a single store-data HID frame into a reading dict.

    Returns:
        {
            "channel_no": int,
            "name": str,       # e.g. "土壤温度"
            "unit": str,       # e.g. "℃"
            "value": float,    # e.g. 24.3
            "timestamp": float # time.time() when parsed
        }

    Raises:
        ValueError: if frame is too short or header is invalid.
    """
    if len(frame) < 50:
        raise ValueError(f"Frame too short: {len(frame)} bytes")

    # Validate header
    if frame[0] != 0xAA or frame[1] != 0x26 or frame[2] != 0x24:
        raise ValueError(
            f"Invalid header: {frame[:3].hex()} (expected AA2624)"
        )

    channel_no = frame[3]

    # ── Extract unit first (needed to decide value scaling) ──────────
    unit = _extract_ascii(frame, 14, window=7)

    # A single digit at offset 14 is metadata, not a real unit
    if len(unit) == 1 and unit.isdigit():
        unit = ""

    # Override unit from channel map if extraction yielded nothing useful
    ch_info = _CHANNEL_MAP.get(channel_no)
    if not unit and ch_info:
        unit = ch_info["unit"]

    # ── Extract value ────────────────────────────────────────────────
    # Primary: big-endian float32 at offset 5.
    float_val = struct.unpack_from(">f", frame, 5)[0]

    if float_val != 0.0:
        value = float_val
    else:
        # Fallback: raw uint16 BE at offset 38-39.
        # Percentage channels store value × 10 (e.g. 152 → 15.2%).
        raw_int = struct.unpack_from(">H", frame, 38)[0]
        if "%" in unit:
            value = raw_int / 10.0
        else:
            value = float(raw_int)

    # ── Extract name ─────────────────────────────────────────────────
    name = _extract_utf8(frame, 21, window=24)
    if not name and ch_info:
        name = ch_info["name"]

    return {
        "channel_no": channel_no,
        "name": name,
        "unit": unit,
        "value": round(value, 2),
        "timestamp": time.time(),
    }


def apply_channel_reading(snapshot: dict, reading: dict) -> None:
    """
    Apply a parsed reading to a snapshot dict, mapping the channel's
    measurement to the correct frontend field name.

    Latest reading always overwrites previous value for the same channel.
    Also maintains a per-channel history in snapshot["_channel_values"].
    """
    channel_no = reading["channel_no"]
    value = reading["value"]
    name = reading["name"]
    ts = reading["timestamp"]

    ch_info = _CHANNEL_MAP.get(channel_no)
    if ch_info:
        field = ch_info["field"]
        snapshot[field] = value

    # Per-channel tracking (used by tests to verify overwrite)
    if "_channel_values" not in snapshot:
        snapshot["_channel_values"] = {}

    snapshot["_channel_values"][name] = {
        "value": value,
        "channel_no": channel_no,
        "timestamp": ts,
    }


def parse_all_frames(frames: list[bytes]) -> dict:
    """
    Parse a list of 64-byte frames and return a merged snapshot dict.
    Latest frame for each channel wins.
    """
    snapshot = {}
    for frame in frames:
        try:
            reading = parse_store_frame(frame)
            apply_channel_reading(snapshot, reading)
        except (ValueError, struct.error) as e:
            print(f"[COS03] Frame parse error: {e}")
    return snapshot
