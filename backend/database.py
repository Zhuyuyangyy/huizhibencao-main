"""
SQLite database module — stores sensor readings for historical queries and AI context.
"""
import os
import sqlite3
import threading
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "sensors.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

_local = threading.local()


def _get_conn() -> sqlite3.Connection:
    """Thread-local database connection"""
    if not hasattr(_local, "conn") or _local.conn is None:
        _local.conn = sqlite3.connect(DB_PATH)
        _local.conn.row_factory = sqlite3.Row
    return _local.conn


def init_db():
    """Create tables if not exist"""
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            -- Greenhouse
            gh_light REAL,
            gh_ph REAL,
            gh_soil_moisture REAL,
            gh_co2 REAL,
            gh_air_humidity REAL,
            gh_air_temp REAL,
            gh_potassium REAL,
            gh_phosphorus REAL,
            gh_ndvi REAL,
            gh_transpiration REAL,
            gh_ec REAL,
            -- Open field
            of_air_temp REAL,
            of_air_humidity REAL,
            of_co2 REAL,
            of_soil_moisture REAL,
            of_rainfall REAL,
            of_wind_speed REAL,
            of_wind_dir TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_readings_ts ON sensor_readings(timestamp);

        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_chat_ts ON chat_history(timestamp);
    """)
    conn.commit()


def save_reading(greenhouse: dict, openfield: dict):
    """Save a sensor reading snapshot"""
    conn = _get_conn()
    conn.execute("""
        INSERT INTO sensor_readings (
            timestamp,
            gh_light, gh_ph, gh_soil_moisture, gh_co2, gh_air_humidity, gh_air_temp,
            gh_potassium, gh_phosphorus, gh_ndvi, gh_transpiration, gh_ec,
            of_air_temp, of_air_humidity, of_co2, of_soil_moisture,
            of_rainfall, of_wind_speed, of_wind_dir
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        greenhouse.get("light"), greenhouse.get("ph"), greenhouse.get("soilMoisture"),
        greenhouse.get("co2"), greenhouse.get("airHumidity"), greenhouse.get("airTemp"),
        greenhouse.get("potassium"), greenhouse.get("phosphorus"), greenhouse.get("ndvi"),
        greenhouse.get("transpiration"), greenhouse.get("ec"),
        openfield.get("airTemp"), openfield.get("airHumidity"), openfield.get("co2"),
        openfield.get("soilMoisture"), openfield.get("rainfall"),
        openfield.get("windSpeed"), openfield.get("windDir"),
    ))
    conn.commit()


def get_recent_readings(minutes: int = 60, limit: int = 200) -> list:
    """Get recent readings for trend analysis"""
    conn = _get_conn()
    since = (datetime.now() - timedelta(minutes=minutes)).isoformat()
    rows = conn.execute(
        "SELECT * FROM sensor_readings WHERE timestamp > ? ORDER BY timestamp DESC LIMIT ?",
        (since, limit)
    ).fetchall()
    return [dict(r) for r in rows]


def get_stats(minutes: int = 60) -> dict:
    """Get min/max/avg stats for recent period"""
    conn = _get_conn()
    since = (datetime.now() - timedelta(minutes=minutes)).isoformat()
    row = conn.execute("""
        SELECT
            COUNT(*) as count,
            MIN(gh_air_temp) as min_temp, MAX(gh_air_temp) as max_temp,
            AVG(gh_air_temp) as avg_temp,
            MIN(gh_air_humidity) as min_humidity, MAX(gh_air_humidity) as max_humidity,
            AVG(gh_air_humidity) as avg_humidity,
            MIN(gh_co2) as min_co2, MAX(gh_co2) as max_co2,
            AVG(gh_co2) as avg_co2,
            MIN(gh_soil_moisture) as min_soil, MAX(gh_soil_moisture) as max_soil,
            AVG(gh_soil_moisture) as avg_soil,
            MIN(gh_light) as min_light, MAX(gh_light) as max_light,
            AVG(gh_light) as avg_light
        FROM sensor_readings WHERE timestamp > ?
    """, (since,)).fetchone()
    return dict(row) if row else {}


def get_ai_context_summary() -> str:
    """Generate a text summary of recent data for AI context"""
    stats = get_stats(minutes=30)
    if not stats or stats.get("count", 0) == 0:
        return "暂无近期传感器数据。"

    return f"""最近30分钟传感器数据统计（共{stats['count']}次采样）：
- 棚内温度: {stats.get('avg_temp', 0):.1f}°C (范围 {stats.get('min_temp', 0):.1f}~{stats.get('max_temp', 0):.1f})
- 棚内湿度: {stats.get('avg_humidity', 0):.1f}% (范围 {stats.get('min_humidity', 0):.1f}~{stats.get('max_humidity', 0):.1f})
- CO₂浓度: {stats.get('avg_co2', 0):.0f} ppm (范围 {stats.get('min_co2', 0):.0f}~{stats.get('max_co2', 0):.0f})
- 土壤湿度: {stats.get('avg_soil', 0):.1f}% (范围 {stats.get('min_soil', 0):.1f}~{stats.get('max_soil', 0):.1f})
- 光照强度: {stats.get('avg_light', 0):.0f} lux (范围 {stats.get('min_light', 0):.0f}~{stats.get('max_light', 0):.0f})"""


def save_chat(role: str, content: str):
    """Save chat message to history"""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO chat_history (timestamp, role, content) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), role, content)
    )
    conn.commit()


def get_recent_chats(limit: int = 20) -> list:
    """Get recent chat history"""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM chat_history ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in reversed(rows)]


# Initialize on import
init_db()
