"""
Sensor data module — matches 壤博士记录仪 (Dr. Soil) data structure.
Supports: 土壤温湿度(3/5层), pH, EC, NPK, 光照, CO₂, etc.
"""
import random
import time
import math
from datetime import datetime
from config import USE_MOCK_DATA

# COS-03 MultiGas reader (lazy import)
_cos03_reader = None
if not USE_MOCK_DATA:
    try:
        from cos03_hid_reader import get_snapshot as cos03_get_snapshot
        from cos03_hid_reader import is_connected as cos03_is_connected
        from cos03_hid_reader import start_reading as cos03_start_reading
        _cos03_reader = True
    except Exception as e:
        print(f"[SensorData] COS-03 reader not available: {e}")

_start_time = time.time()


def _drift(base, amp, period=300):
    t = time.time() - _start_time
    return base + amp * math.sin(t * 2 * math.pi / period) + random.uniform(-amp * 0.08, amp * 0.08)


# ==================== 土壤传感器数据 (壤博士) ====================

def get_soil_moisture_5layer() -> dict:
    """5层土壤湿度 — 壤博士核心数据"""
    return {
        "layer1": round(_drift(42.3, 3), 1),   # 表层 0-20cm
        "layer2": round(_drift(38.7, 2.5), 1),  # 20-40cm
        "layer3": round(_drift(35.2, 2), 1),    # 40-60cm
        "layer4": round(_drift(31.8, 1.5), 1),  # 60-80cm
        "layer5": round(_drift(28.5, 1), 1),    # 80-100cm
        "average": 0,  # calculated below
    }


def get_soil_temp_moisture_5layer() -> dict:
    """5层土壤温湿度"""
    layers = []
    for i, (t_base, m_base) in enumerate([
        (24.5, 42.3), (22.8, 38.7), (21.2, 35.2),
        (20.1, 31.8), (19.3, 28.5)
    ]):
        layers.append({
            "depth": f"{(i+1)*20}cm",
            "temperature": round(_drift(t_base, 1.5), 1),
            "moisture": round(_drift(m_base, 2.5), 1),
        })
    return {"layers": layers}


def get_soil_moisture_3layer() -> dict:
    """3层土壤湿度"""
    return {
        "layer1": round(_drift(40.1, 3), 1),
        "layer2": round(_drift(34.5, 2), 1),
        "layer3": round(_drift(29.8, 1.5), 1),
        "average": 0,
    }


def get_soil_temp_moisture_3layer() -> dict:
    """3层土壤温湿度"""
    layers = []
    for i, (t_base, m_base) in enumerate([
        (23.8, 40.1), (21.5, 34.5), (19.8, 29.8)
    ]):
        layers.append({
            "depth": f"{(i+1)*30}cm",
            "temperature": round(_drift(t_base, 1.5), 1),
            "moisture": round(_drift(m_base, 2), 1),
        })
    return {"layers": layers}


def get_soil_ph() -> dict:
    """土壤pH"""
    return {
        "value": round(_drift(6.38, 0.3), 2),
        "status": "酸性" if _drift(6.38, 0.3) < 6.5 else "中性" if _drift(6.38, 0.3) < 7.5 else "碱性",
    }


def get_soil_ec() -> dict:
    """土壤电导率 (EC)"""
    val = round(_drift(1.2, 0.2), 2)
    return {
        "value": val,
        "unit": "mS/cm",
        "status": "正常" if val < 2.0 else "偏高" if val < 4.0 else "过高",
    }


def get_npk() -> dict:
    """氮磷钾三合一"""
    return {
        "nitrogen": round(_drift(125, 15), 1),      # mg/kg
        "phosphorus": round(_drift(42.5, 5), 1),     # mg/kg
        "potassium": round(_drift(168, 20), 1),      # mg/kg
        "nitrogen_unit": "mg/kg",
        "phosphorus_unit": "mg/kg",
        "potassium_unit": "mg/kg",
    }


# ==================== 环境传感器数据 ====================

def get_greenhouse_data() -> dict:
    """有棚区完整传感器数据 — COS-03 优先，无设备时回退模拟数据"""
    if _cos03_reader and not USE_MOCK_DATA:
        try:
            cos03_snap = cos03_get_snapshot()
            if cos03_snap and cos03_is_connected():
                # cos03_snap already contains frontend field names
                # (airTemp, soilMoisture, etc.) via cos03_reader._CHANNEL_MAP
                result = {}
                for k, v in cos03_snap.items():
                    if k.startswith("_"):
                        continue
                    result[k] = round(v, 2) if isinstance(v, float) else v
                # Fill in fields the COS-03 doesn't measure (ndvi, transpiration)
                # so the frontend always gets a complete dict
                for field in ("ndvi", "transpiration"):
                    if field not in result:
                        result[field] = round(_drift(
                            {"ndvi": 0.72, "transpiration": 4.5}[field], 0.05
                            if field == "ndvi" else 0.8), 2)
                return result
        except Exception:
            pass

    return {
        "airTemp": round(_drift(26.4, 2), 1),
        "airHumidity": round(_drift(68.2, 5), 1),
        "light": round(_drift(15800, 1500), 0),
        "co2": round(_drift(613, 50), 0),
        "soilMoisture": round(_drift(32.6, 5), 1),
        "ph": round(_drift(6.38, 0.3), 2),
        "ec": round(_drift(1.2, 0.2), 2),
        "potassium": round(_drift(28.6, 3), 1),
        "phosphorus": round(_drift(192, 20), 0),
        "ndvi": round(_drift(0.72, 0.05), 2),
        "transpiration": round(_drift(4.5, 0.8), 1),
    }


def get_openfield_data() -> dict:
    """无棚区传感器数据"""
    return {
        "airTemp": round(_drift(28.6, 2), 1),
        "airHumidity": round(_drift(72.5, 5), 1),
        "co2": round(_drift(420, 30), 0),
        "soilMoisture": round(_drift(45.2, 5), 1),
        "rainfall": 0,
        "windSpeed": round(_drift(2.3, 1.5), 1),
        "windDir": "东南",
    }


# ==================== 设备管理 (壤博士功能) ====================

def get_device_info() -> dict:
    """设备信息 — 对应壤博士的"设备信息"页面"""
    return {
        "deviceName": "壤博士多参数记录仪",
        "deviceType": "RK-5000-TR",
        "softwareVersion": "V2.3.1",
        "hardwareVersion": "V1.0",
        "companyName": "山东仁科测控技术有限公司",
        "productionDate": "2024-06-15",
        "serialNumber": "RK20240615001",
        "batteryLevel": 85,
        "currentStatus": "在线",
        "recordingStatus": "正在记录",
        "recordingInterval": 30,  # 秒
        "storedRecords": 12847,
        "maxStorage": 65535,
        "alarmEnabled": True,
        "soundEnabled": True,
        "screenTimeout": 30,  # 秒
    }


def get_device_list() -> list:
    """大棚内设备列表"""
    return [
        {"id": "fan", "name": "通风系统", "status": "on", "value": 65, "category": "ventilation", "icon": "wind",
         "modbusAddr": 1, "baudRate": 9600},
        {"id": "light", "name": "LED补光灯", "status": "on", "value": 60, "category": "lighting", "icon": "sun",
         "modbusAddr": 2, "baudRate": 9600},
        {"id": "water", "name": "智能水肥机", "status": "running", "value": 28, "category": "irrigation", "icon": "droplet",
         "modbusAddr": 3, "baudRate": 9600},
        {"id": "shade", "name": "遮阳帘", "status": "off", "value": 0, "category": "shading", "icon": "cloud",
         "modbusAddr": 4, "baudRate": 9600},
        {"id": "heater", "name": "加热系统", "status": "off", "value": 0, "category": "heating", "icon": "thermometer",
         "modbusAddr": 5, "baudRate": 9600},
        {"id": "co2_gen", "name": "CO₂发生器", "status": "on", "value": 45, "category": "co2", "icon": "wind",
         "modbusAddr": 6, "baudRate": 9600},
    ]


# ==================== 报警管理 (壤博士功能) ====================

# 报警阈值配置
_alarm_thresholds = {
    "airTemp": {"min": 15, "max": 35, "minMin": 5, "maxMax": 45, "name": "空气温度", "unit": "°C"},
    "airHumidity": {"min": 40, "max": 80, "minMin": 20, "maxMax": 95, "name": "空气湿度", "unit": "%"},
    "soilMoisture": {"min": 25, "max": 65, "minMin": 15, "maxMax": 80, "name": "土壤湿度", "unit": "%"},
    "co2": {"min": 300, "max": 1000, "minMin": 200, "maxMax": 1500, "name": "CO₂浓度", "unit": "ppm"},
    "ph": {"min": 5.5, "max": 7.5, "minMin": 4.5, "maxMax": 8.5, "name": "土壤pH", "unit": ""},
    "ec": {"min": 0.5, "max": 2.0, "minMin": 0.2, "maxMax": 4.0, "name": "电导率", "unit": "mS/cm"},
    "light": {"min": 8000, "max": 25000, "minMin": 3000, "maxMax": 40000, "name": "光照强度", "unit": "lux"},
}

_alerts = [
    {"id": 1, "type": "pest", "message": "钻心虫声学信号增强", "desc": "虫害声学识别模型检测到钻心虫活动信号增强，建议加强监测并考虑生物防治。", "time": "14:34:42", "severity": "warning"},
    {"id": 2, "type": "env", "message": "棚内湿度偏高", "desc": "当前空气湿度68.2%，超出适宜范围（50-65%），建议开启通风系统。", "time": "14:28:15", "severity": "warning"},
    {"id": 3, "type": "device", "message": "水肥机管道压力异常", "desc": "水肥机输出管道压力为0.42MPa，超出正常范围，建议检查管道是否堵塞。", "time": "14:15:00", "severity": "danger"},
    {"id": 4, "type": "env", "message": "光照强度波动较大", "desc": "过去30分钟光照强度在12000-18500lux间波动，建议检查补光灯运行状态。", "time": "13:55:30", "severity": "info"},
]


def get_alarm_thresholds() -> dict:
    """获取报警阈值配置"""
    return _alarm_thresholds


def update_alarm_threshold(key: str, min_val=None, max_val=None) -> dict:
    """更新报警阈值"""
    if key in _alarm_thresholds:
        if min_val is not None:
            _alarm_thresholds[key]["min"] = min_val
        if max_val is not None:
            _alarm_thresholds[key]["max"] = max_val
        return {"code": 0, "msg": "更新成功"}
    return {"code": 1, "msg": f"未知参数: {key}"}


def check_alarms(data: dict) -> list:
    """根据当前数据检查是否触发报警"""
    triggered = []
    now = datetime.now().strftime("%H:%M:%S")
    for key, threshold in _alarm_thresholds.items():
        val = data.get(key)
        if val is None:
            continue
        if val < threshold["min"]:
            triggered.append({
                "id": f"alarm_{key}_low",
                "type": "env",
                "message": f"{threshold['name']}偏低: {val}{threshold['unit']}",
                "desc": f"当前{threshold['name']}为{val}{threshold['unit']}，低于下限{threshold['min']}{threshold['unit']}",
                "time": now,
                "severity": "warning",
            })
        elif val > threshold["max"]:
            triggered.append({
                "id": f"alarm_{key}_high",
                "type": "env",
                "message": f"{threshold['name']}偏高: {val}{threshold['unit']}",
                "desc": f"当前{threshold['name']}为{val}{threshold['unit']}，超出上限{threshold['max']}{threshold['unit']}",
                "time": now,
                "severity": "warning",
            })
    return triggered


# ==================== 综合数据 ====================

def get_radar_data() -> list:
    gh = get_greenhouse_data()
    return [
        {"subject": "光照(lux)", "A": gh["light"], "fullMark": 20000, "unit": " lux"},
        {"subject": "pH值", "A": gh["ph"], "fullMark": 14, "unit": ""},
        {"subject": "土壤湿度", "A": gh["soilMoisture"], "fullMark": 100, "unit": "%"},
        {"subject": "CO₂浓度", "A": gh["co2"], "fullMark": 1000, "unit": " ppm"},
        {"subject": "空气湿度", "A": gh["airHumidity"], "fullMark": 100, "unit": "%"},
        {"subject": "空气温度", "A": gh["airTemp"], "fullMark": 50, "unit": "°C"},
        {"subject": "钾(K)", "A": gh["potassium"], "fullMark": 100, "unit": "%"},
        {"subject": "磷(P)", "A": gh["phosphorus"], "fullMark": 300, "unit": " mg/kg"},
    ]


def get_snapshot() -> dict:
    return {
        "timestamp": datetime.now().isoformat(),
        "greenhouse": get_greenhouse_data(),
        "openfield": get_openfield_data(),
        "devices": get_device_list(),
        "alerts": get_alerts(),
        "soil_5layer": get_soil_moisture_5layer(),
        "soil_ph": get_soil_ph(),
        "soil_ec": get_soil_ec(),
        "npk": get_npk(),
    }


def get_alerts() -> list:
    return _alerts


def save_to_db():
    try:
        from database import save_reading
        save_reading(get_greenhouse_data(), get_openfield_data())
    except Exception as e:
        print(f"[SensorData] DB save error: {e}")
