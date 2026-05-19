"""
USB HID Device Scanner
Run this script to find all connected HID devices.
We need the vendor_id and product_id to read sensor data.
"""
import sys

try:
    import hid
except ImportError:
    print("正在安装 hidapi 库...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "hidapi", "--break-system-packages"])
    import hid


def scan_devices():
    """Scan and list all connected HID devices"""
    print("=" * 70)
    print("  USB HID 设备扫描器")
    print("=" * 70)
    print()

    devices = hid.enumerate()

    if not devices:
        print("未检测到任何 HID 设备。")
        print("请确保传感器设备已通过 USB 连接。")
        return

    print(f"检测到 {len(devices)} 个 HID 设备:\n")
    print(f"{'#':<4} {'厂商ID':<10} {'产品ID':<10} {'厂商':<25} {'产品':<30} {'使用量'}")
    print("-" * 90)

    for i, d in enumerate(devices):
        vendor_id = d.get('vendor_id', 0)
        product_id = d.get('product_id', 0)
        manufacturer = d.get('manufacturer_string', '未知')
        product = d.get('product_string', '未知')
        usage = d.get('usage', 0)
        usage_page = d.get('usage_page', 0)

        print(f"{i+1:<4} 0x{vendor_id:04X}    0x{product_id:04X}    {manufacturer:<25} {product:<30} {usage_page:04X}:{usage:04X}")

    print()
    print("=" * 70)
    print("请将上面的厂商ID和产品ID告诉我，我来配置读取逻辑。")
    print("如果你知道哪个是传感器设备，也可以直接告诉我设备名称。")
    print("=" * 70)


if __name__ == "__main__":
    scan_devices()
