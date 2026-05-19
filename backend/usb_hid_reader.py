"""
USB HID Reader — reads sensor data directly from USB HID devices.
Replace mock data in sensor_data.py with real readings.

Setup:
  1. Run scan_usb_devices.py to find your device's vendor_id and product_id
  2. Set them in config.py
  3. This module will read data automatically
"""
import sys
import struct
import threading
import time

try:
    import hid
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "hidapi", "--break-system-packages"])
    import hid

from config import (
    USB_VENDOR_ID, USB_PRODUCT_ID,
    USB_DATA_FORMAT, USB_READ_INTERVAL,
)

_running = False
_thread = None
_latest_data = {}


def _parse_data(raw_bytes: bytes) -> dict:
    """
    Parse raw HID report bytes into sensor values.
    Adjust this based on your device's actual data format.

    Common formats:
    - 6 bytes: 2 bytes each for temp, humidity, co2 (big-endian uint16)
    - 8 bytes: 4 float values
    - Custom: depends on device protocol
    """
    try:
        if USB_DATA_FORMAT == "2byte_xyz":
            # Example: 6 bytes = 3 x uint16 (temp, humidity, co2)
            if len(raw_bytes) >= 6:
                return {
                    "airTemp": struct.unpack(">H", raw_bytes[0:2])[0] / 100.0,
                    "airHumidity": struct.unpack(">H", raw_bytes[2:4])[0] / 100.0,
                    "co2": struct.unpack(">H", raw_bytes[4:6])[0],
                }

        elif USB_DATA_FORMAT == "float4":
            # Example: 16 bytes = 4 x float32
            if len(raw_bytes) >= 16:
                vals = struct.unpack(">4f", raw_bytes[0:16])
                return {
                    "airTemp": round(vals[0], 1),
                    "airHumidity": round(vals[1], 1),
                    "co2": round(vals[2], 0),
                    "soilMoisture": round(vals[3], 1),
                }

        elif USB_DATA_FORMAT == "raw_hex":
            # Example: raw hex string like "001A2B3C..."
            # Just return raw hex for debugging
            return {"raw": raw_bytes.hex()}

        else:
            # Default: try to interpret as temperature + humidity
            if len(raw_bytes) >= 4:
                return {
                    "raw_bytes": list(raw_bytes),
                    "airTemp": raw_bytes[0] + raw_bytes[1] / 100.0 if len(raw_bytes) > 1 else 0,
                    "airHumidity": raw_bytes[2] + raw_bytes[3] / 100.0 if len(raw_bytes) > 3 else 0,
                }

    except Exception as e:
        return {"error": str(e), "raw": raw_bytes.hex() if raw_bytes else ""}

    return {"raw": raw_bytes.hex() if raw_bytes else "", "note": "未识别的数据格式"}


def _read_loop():
    """Background thread that continuously reads from HID device"""
    global _latest_data, _running

    device = hid.device()
    try:
        device.open(USB_VENDOR_ID, USB_PRODUCT_ID)
        device.set_nonblocking(True)
        print(f"[USB] 已连接设备 0x{USB_VENDOR_ID:04X}:0x{USB_PRODUCT_ID:04X}")

        while _running:
            try:
                # HID read: returns list of ints (bytes)
                data = device.read(64, timeout=1000)
                if data and len(data) > 0:
                    raw = bytes(data)
                    parsed = _parse_data(raw)
                    parsed["_timestamp"] = time.time()
                    parsed["_raw_hex"] = raw.hex()
                    _latest_data = parsed
                    print(f"[USB] 读取: {parsed}")
            except Exception as e:
                if _running:
                    print(f"[USB] 读取错误: {e}")
                    time.sleep(1)

    except Exception as e:
        print(f"[USB] 连接失败: {e}")
        print("[USB] 请检查设备是否已连接，vendor_id/product_id 是否正确")
    finally:
        try:
            device.close()
        except:
            pass


def start_reading():
    """Start background USB HID reading"""
    global _running, _thread
    if _running:
        return
    _running = True
    _thread = threading.Thread(target=_read_loop, daemon=True)
    _thread.start()
    print("[USB] 后台读取已启动")


def stop_reading():
    """Stop background reading"""
    global _running
    _running = False
    print("[USB] 后台读取已停止")


def get_latest_data() -> dict:
    """Get the most recent reading from the device"""
    return _latest_data


def is_connected() -> bool:
    """Check if device is connected and returning data"""
    if not _latest_data:
        return False
    ts = _latest_data.get("_timestamp", 0)
    return (time.time() - ts) < 5  # Connected if data is less than 5s old
