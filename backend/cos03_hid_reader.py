"""
COS-03 MultiGas HID Reader — sends vendor command, collects response
frames, parses them via cos03_reader, and stores the merged snapshot.

Thread-safe: snapshot is updated atomically; readers call get_snapshot().
"""
import sys
import threading
import time

try:
    import hid
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "hidapi",
                           "--break-system-packages"])
    import hid

from config import USB_VENDOR_ID, USB_PRODUCT_ID, USB_READ_INTERVAL
from cos03_reader import parse_all_frames

# ── Vendor command: "读取存储数据" (store-data read) ────────────────
# 64-byte HID output report.  Byte 0 = report-id 0x55.
_CMD_STORE_READ = bytes([
    0x55, 0x01, 0x23,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0xE6, 0x7A,
])

# ── Module state ────────────────────────────────────────────────────
_running = False
_thread: threading.Thread | None = None
_snapshot: dict = {}
_snapshot_lock = threading.Lock()
_connected = False
_last_read_ts = 0.0


def _request_frames(device: hid.device, timeout_ms: int = 500) -> list[bytes]:
    """
    Send the store-read command and collect all response frames
    until no new frame arrives within *timeout_ms*.
    """
    frames: list[bytes] = []

    # Send vendor command
    device.write(_CMD_STORE_READ)

    # Collect response frames — each is 64 bytes starting with AA 26 24
    while True:
        try:
            data = device.read(64, timeout=timeout_ms)
            if not data:
                break  # timeout — no more frames
            raw = bytes(data)
            if len(raw) >= 3 and raw[0] == 0xAA and raw[1] == 0x26 and raw[2] == 0x24:
                frames.append(raw)
            else:
                # Not a valid COS-03 frame — might be echo or noise
                break
        except Exception:
            break

    return frames


def _read_loop():
    """Background thread: periodically request frames and update snapshot."""
    global _connected, _last_read_ts, _snapshot

    device = hid.device()
    try:
        device.open(USB_VENDOR_ID, USB_PRODUCT_ID)
        device.set_nonblocking(True)
        _connected = True
        print(f"[COS03] 已连接设备 0x{USB_VENDOR_ID:04X}:0x{USB_PRODUCT_ID:04X}")
    except Exception as e:
        _connected = False
        print(f"[COS03] 连接失败: {e}")
        print("[COS03] 请检查设备是否已连接，或在 config.py 中确认 VID/PID")
        return

    try:
        while _running:
            try:
                frames = _request_frames(device, timeout_ms=500)
                if frames:
                    new_snap = parse_all_frames(frames)
                    if new_snap:
                        with _snapshot_lock:
                            _snapshot.update(new_snap)
                            _last_read_ts = time.time()
                        ch_names = list(new_snap.get("_channel_values", {}).keys())
                        print(f"[COS03] 读取 {len(frames)} 帧, 通道: {ch_names}")
                else:
                    print("[COS03] 本次无有效帧返回")
            except Exception as e:
                if _running:
                    print(f"[COS03] 读取错误: {e}")
                    _connected = False

            time.sleep(USB_READ_INTERVAL)

    finally:
        try:
            device.close()
        except Exception:
            pass
        _connected = False
        print("[COS03] 设备已断开")


def start_reading():
    """Start the COS-03 background polling thread."""
    global _running, _thread
    if _running:
        return
    _running = True
    _thread = threading.Thread(target=_read_loop, daemon=True, name="cos03-reader")
    _thread.start()
    print("[COS03] 后台轮询已启动")


def stop_reading():
    """Stop the background polling thread."""
    global _running
    _running = False
    print("[COS03] 后台轮询已停止")


def get_snapshot() -> dict:
    """
    Return the latest merged sensor snapshot.
    Keys are frontend field names (airTemp, soilMoisture, etc.)
    plus _channel_values for debug.
    """
    with _snapshot_lock:
        return dict(_snapshot)


def is_connected() -> bool:
    """True if we have received data within the last 10 seconds."""
    if not _connected:
        return False
    return (time.time() - _last_read_ts) < 10
