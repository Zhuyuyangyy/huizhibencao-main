"""Quick verification of cos03_reader against test frames."""
import struct
import sys
sys.path.insert(0, '.')

from cos03_reader import parse_store_frame, apply_channel_reading

SOIL_TEMP_FRAME = bytes.fromhex(
    "AA2624020141C266666A0856E702E2848300000000E59C9FE5A3A4E6B8A9E5BAA6"
    "000000000000AF00000000000000000000000000000000000000000000698F"
)
SOIL_MOISTURE_FRAME = bytes.fromhex(
    "AA26240101000000006A0857960025524800000000E59C9FE5A3A4E6B9BFE5BAA6"
    "0000000000009800000000000000000000000000000000000000000000EB53"
)
PH_FRAME = bytes.fromhex(
    "AA26240401404000006A0858450030000000000000504800000000000000000000"
    "000000000000870000000000000000000000000000000000000000000000EBE7"
)
LEAF_MOISTURE_FRAME = bytes.fromhex(
    "AA26240801000000006A0857EB0025000000000000E58FB6E99DA2E6B9BFE5BAA6"
    "0000000000007700000000000000000000000000000000000000000000A054"
)
NITROGEN_FRAME = bytes.fromhex(
    "AA26240501000000006A08573C006D672F6B670000E6B0AE000000000000000000"
    "00000000000000900000000000000000000000000000000000000000000D74D"
)

print("=== Frame Analysis ===")
for name, frame in [
    ("SOIL_TEMP", SOIL_TEMP_FRAME),
    ("SOIL_MOISTURE", SOIL_MOISTURE_FRAME),
    ("PH", PH_FRAME),
    ("LEAF_MOISTURE", LEAF_MOISTURE_FRAME),
    ("NITROGEN", NITROGEN_FRAME),
]:
    print(f"\n--- {name} ---")
    print(f"  Byte 3 (channel): 0x{frame[3]:02X} = {frame[3]}")
    val_be = struct.unpack_from(">f", frame, 5)[0]
    print(f"  Float@5 BE: {val_be:.4f}")
    val_le = struct.unpack_from("<f", frame, 5)[0]
    print(f"  Float@5 LE: {val_le:.4f}")

    # Name at offset 21
    name_raw = frame[21:45]
    name_end = name_raw.find(0x00)
    if name_end == -1:
        name_end = len(name_raw)
    try:
        name_str = name_raw[:name_end].decode("utf-8")
    except:
        name_str = f"<decode error: {name_raw[:name_end].hex()}>"
    print(f"  Name@21: '{name_str}'")

    # Unit at offset 17
    unit_raw = frame[17:21]
    unit_end = unit_raw.find(0x00)
    if unit_end == -1:
        unit_end = len(unit_raw)
    try:
        unit_str = unit_raw[:unit_end].decode("ascii")
    except:
        unit_str = f"<decode error: {unit_raw[:unit_end].hex()}>"
    print(f"  Unit@17: '{unit_str}'")

print("\n=== Running parse_store_frame ===")
for name, frame, expected_val in [
    ("SOIL_TEMP", SOIL_TEMP_FRAME, 24.3),
    ("SOIL_MOISTURE", SOIL_MOISTURE_FRAME, 15.2),
    ("PH", PH_FRAME, 3.0),
    ("LEAF_MOISTURE", LEAF_MOISTURE_FRAME, 11.9),
    ("NITROGEN", NITROGEN_FRAME, 144.0),
]:
    r = parse_store_frame(frame)
    match = abs(r["value"] - expected_val) < 0.5
    status = "PASS" if match else "FAIL"
    print(f"  {status} {name}: ch={r['channel_no']}, name='{r['name']}', "
          f"unit='{r['unit']}', value={r['value']} (expected {expected_val})")

print("\n=== Running apply_channel_reading ===")
snapshot = {}
for frame in [SOIL_TEMP_FRAME, SOIL_MOISTURE_FRAME, PH_FRAME, LEAF_MOISTURE_FRAME, NITROGEN_FRAME]:
    r = parse_store_frame(frame)
    apply_channel_reading(snapshot, r)

print(f"  snapshot keys: {[k for k in snapshot if not k.startswith('_')]}")
print(f"  channel_values: {snapshot.get('_channel_values', {})}")
