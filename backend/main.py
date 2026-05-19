"""
慧植本草 — Backend API Server
FastAPI application with sensor data, Excel export, and AI chat.
"""
import os
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler

from config import CORS_ORIGINS, EXCEL_EXPORT_INTERVAL_MINUTES, EXCEL_EXPORT_DIR
from sensor_data import (
    get_greenhouse_data, get_openfield_data, get_device_list,
    get_alerts, get_radar_data, get_snapshot, save_to_db,
    get_device_info, get_soil_moisture_5layer, get_soil_temp_moisture_5layer,
    get_soil_moisture_3layer, get_soil_temp_moisture_3layer,
    get_soil_ph, get_soil_ec, get_npk,
    get_alarm_thresholds, update_alarm_threshold, check_alarms,
)
from excel_export import auto_export_task, export_to_excel
from ai_chat import AIServiceError, chat_with_sage
from database import get_recent_readings, get_stats

# === Scheduler ===
scheduler = BackgroundScheduler()


def _db_save_task():
    """Periodic task: save current readings to database"""
    save_to_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle"""
    # Initialize database
    from database import init_db
    init_db()
    print("[Startup] Database initialized")

    # Record initial snapshot
    from excel_export import _record_snapshot
    _record_snapshot()

    # Save to database every 30 seconds
    scheduler.add_job(
        _db_save_task,
        "interval",
        seconds=30,
        id="db_save",
        replace_existing=True,
    )

    # Auto-export Excel every N minutes
    scheduler.add_job(
        auto_export_task,
        "interval",
        minutes=EXCEL_EXPORT_INTERVAL_MINUTES,
        id="auto_excel_export",
        replace_existing=True,
    )
    scheduler.start()
    print(f"[Startup] DB save every 30s, Excel export every {EXCEL_EXPORT_INTERVAL_MINUTES}min")
    print(f"[Startup] Export directory: {EXCEL_EXPORT_DIR}")

    # Start COS-03 MultiGas sensor reader (if device connected)
    from config import USE_MOCK_DATA
    if not USE_MOCK_DATA:
        try:
            from cos03_hid_reader import start_reading as cos03_start
            cos03_start()
            print("[Startup] COS-03 MultiGas reader started")
        except Exception as e:
            print(f"[Startup] COS-03 reader not started: {e}")
    else:
        print("[Startup] Running in MOCK mode — COS-03 reader skipped")

    yield

    scheduler.shutdown()
    print("[Shutdown] Scheduler stopped")

    # Stop COS-03 reader
    try:
        from cos03_hid_reader import stop_reading as cos03_stop
        cos03_stop()
    except Exception:
        pass


app = FastAPI(
    title="慧植本草 API",
    description="中医智慧农业后端服务 — 传感器数据、Excel导出、本草精灵AI",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# ==================== Sensor Data APIs ====================

@app.get("/api/greenhouse")
async def api_greenhouse():
    """有棚区传感器数据"""
    return {"code": 0, "data": get_greenhouse_data(), "ts": datetime.now().isoformat()}


@app.get("/api/openfield")
async def api_openfield():
    """无棚区传感器数据"""
    return {"code": 0, "data": get_openfield_data(), "ts": datetime.now().isoformat()}


@app.get("/api/devices")
async def api_devices():
    """设备列表与状态"""
    return {"code": 0, "data": get_device_list()}


@app.get("/api/alerts")
async def api_alerts():
    """告警列表"""
    return {"code": 0, "data": get_alerts()}


@app.get("/api/radar")
async def api_radar():
    """雷达图数据"""
    return {"code": 0, "data": get_radar_data()}


@app.get("/api/snapshot")
async def api_snapshot():
    """完整数据快照"""
    return {"code": 0, "data": get_snapshot()}


# ==================== 壤博士 — 土壤传感器 APIs ====================

@app.get("/api/soil/moisture/5layer")
async def api_soil_moisture_5layer():
    """5层土壤湿度"""
    data = get_soil_moisture_5layer()
    data["average"] = round((data["layer1"] + data["layer2"] + data["layer3"] + data["layer4"] + data["layer5"]) / 5, 1)
    return {"code": 0, "data": data}


@app.get("/api/soil/temp-moisture/5layer")
async def api_soil_temp_moisture_5layer():
    """5层土壤温湿度"""
    return {"code": 0, "data": get_soil_temp_moisture_5layer()}


@app.get("/api/soil/moisture/3layer")
async def api_soil_moisture_3layer():
    """3层土壤湿度"""
    data = get_soil_moisture_3layer()
    data["average"] = round((data["layer1"] + data["layer2"] + data["layer3"]) / 3, 1)
    return {"code": 0, "data": data}


@app.get("/api/soil/temp-moisture/3layer")
async def api_soil_temp_moisture_3layer():
    """3层土壤温湿度"""
    return {"code": 0, "data": get_soil_temp_moisture_3layer()}


@app.get("/api/soil/ph")
async def api_soil_ph():
    """土壤pH"""
    return {"code": 0, "data": get_soil_ph()}


@app.get("/api/soil/ec")
async def api_soil_ec():
    """土壤电导率"""
    return {"code": 0, "data": get_soil_ec()}


@app.get("/api/soil/npk")
async def api_soil_npk():
    """氮磷钾三合一"""
    return {"code": 0, "data": get_npk()}


@app.get("/api/soil/all")
async def api_soil_all():
    """所有土壤传感器数据汇总"""
    return {"code": 0, "data": {
        "moisture_5layer": get_soil_moisture_5layer(),
        "temp_moisture_5layer": get_soil_temp_moisture_5layer(),
        "ph": get_soil_ph(),
        "ec": get_soil_ec(),
        "npk": get_npk(),
    }}


# ==================== 壤博士 — 设备管理 APIs ====================

@app.get("/api/device/info")
async def api_device_info():
    """设备信息（壤博士风格）"""
    return {"code": 0, "data": get_device_info()}


@app.post("/api/device/time-sync")
async def api_device_time_sync():
    """时间同步"""
    return {"code": 0, "msg": "时间同步成功", "time": datetime.now().isoformat()}


@app.post("/api/device/restart")
async def api_device_restart():
    """设备重启"""
    return {"code": 0, "msg": "重启指令已发送"}


# ==================== 壤博士 — 报警阈值 APIs ====================

@app.get("/api/alarm/thresholds")
async def api_alarm_thresholds():
    """获取报警阈值配置"""
    return {"code": 0, "data": get_alarm_thresholds()}


class ThresholdUpdate(BaseModel):
    min: float = None
    max: float = None


@app.put("/api/alarm/thresholds/{key}")
async def api_update_threshold(key: str, req: ThresholdUpdate):
    """更新报警阈值"""
    return update_alarm_threshold(key, req.min, req.max)


@app.get("/api/alarm/check")
async def api_alarm_check():
    """检查当前数据是否触发报警"""
    gh = get_greenhouse_data()
    triggered = check_alarms(gh)
    return {"code": 0, "data": triggered, "count": len(triggered)}


# ==================== Historical Data APIs ====================

@app.get("/api/history")
async def api_history(minutes: int = 60, limit: int = 200):
    """获取历史传感器数据"""
    data = get_recent_readings(minutes=minutes, limit=limit)
    return {"code": 0, "data": data, "count": len(data)}


@app.get("/api/stats")
async def api_stats(minutes: int = 60):
    """获取统计信息（min/max/avg）"""
    data = get_stats(minutes=minutes)
    return {"code": 0, "data": data}


# ==================== Excel Export APIs ====================

@app.get("/api/export/excel")
async def api_export_excel():
    """手动触发Excel导出"""
    try:
        path = export_to_excel()
        filename = os.path.basename(path)
        return FileResponse(
            path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")


@app.get("/api/export/list")
async def api_export_list():
    """列出已导出的Excel文件"""
    if not os.path.exists(EXCEL_EXPORT_DIR):
        return {"code": 0, "data": []}
    files = []
    for f in sorted(os.listdir(EXCEL_EXPORT_DIR), reverse=True):
        if f.endswith(".xlsx"):
            filepath = os.path.join(EXCEL_EXPORT_DIR, f)
            files.append({
                "name": f,
                "size": os.path.getsize(filepath),
                "time": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat(),
            })
    return {"code": 0, "data": files[:50]}


@app.get("/api/export/download/{filename}")
async def api_export_download(filename: str):
    """下载指定的Excel文件"""
    filepath = os.path.join(EXCEL_EXPORT_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(filepath, filename=filename)


# ==================== AI Chat API ====================

class ChatRequest(BaseModel):
    question: str
    withContext: bool = True  # Whether to include sensor data context


@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    """本草精灵AI对话"""
    try:
        sensor_context = get_snapshot() if req.withContext else None
    except Exception as e:
        print(f"[Chat] get_snapshot error: {e}", flush=True)
        sensor_context = None
    try:
        reply = await chat_with_sage(req.question, sensor_context)
    except AIServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.user_message) from exc
    except Exception as exc:
        print(f"[Chat] Unexpected error: {exc}", flush=True)
        raise HTTPException(status_code=500, detail=f"对话服务异常: {exc}") from exc
    return {
        "code": 0,
        "data": {
            "role": "sage",
            "content": reply,
            "timestamp": datetime.now().isoformat(),
        }
    }


@app.get("/api/health")
async def api_health():
    """健康检查"""
    return {"status": "ok", "time": datetime.now().isoformat()}


@app.get("/api/sensor/status")
async def api_sensor_status():
    """传感器连接状态"""
    from config import USE_MOCK_DATA
    if USE_MOCK_DATA:
        return {"code": 0, "data": {"mode": "mock", "connected": False}}
    try:
        from cos03_hid_reader import is_connected as cos03_ok
        return {"code": 0, "data": {"mode": "cos03", "connected": cos03_ok()}}
    except Exception:
        return {"code": 0, "data": {"mode": "unknown", "connected": False}}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
