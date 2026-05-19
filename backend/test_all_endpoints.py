"""一键测试所有后端 API 接口"""
import sys, json
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

endpoints = [
    "GET  /api/health",
    "GET  /api/greenhouse",
    "GET  /api/openfield",
    "GET  /api/devices",
    "GET  /api/alerts",
    "GET  /api/radar",
    "GET  /api/snapshot",
    "GET  /api/soil/moisture/5layer",
    "GET  /api/soil/temp-moisture/5layer",
    "GET  /api/soil/moisture/3layer",
    "GET  /api/soil/temp-moisture/3layer",
    "GET  /api/soil/ph",
    "GET  /api/soil/ec",
    "GET  /api/soil/npk",
    "GET  /api/soil/all",
    "GET  /api/device/info",
    "GET  /api/alarm/thresholds",
    "GET  /api/alarm/check",
    "GET  /api/sensor/status",
    "GET  /api/history?minutes=5",
    "GET  /api/stats?minutes=5",
    "GET  /api/export/list",
]

passed = 0
failed = 0

print("=" * 60)
print("  后端 API 接口测试")
print("=" * 60)

for ep in endpoints:
    method, path = ep.split(maxsplit=1)
    try:
        resp = client.get(path)
        data = resp.json()
        status = resp.status_code
        code = data.get("code", "N/A")

        if status == 200 and (code == 0 or code == "ok" or "status" in data):
            passed += 1
            print(f"  ✓ {status} {path}  code={code}")
        else:
            failed += 1
            print(f"  ✗ {status} {path}  code={code}  data_keys={list(data.keys())[:5]}")
    except Exception as e:
        failed += 1
        print(f"  ✗ {path}  ERROR: {e}")

# Test POST endpoints
print("\n--- POST 端点 ---")
try:
    resp = client.post("/api/device/time-sync")
    data = resp.json()
    passed += 1
    print(f"  ✓ {resp.status_code} /api/device/time-sync  msg={data.get('msg','')}")
except Exception as e:
    failed += 1
    print(f"  ✗ /api/device/time-sync  ERROR: {e}")

try:
    resp = client.post("/api/device/restart")
    data = resp.json()
    passed += 1
    print(f"  ✓ {resp.status_code} /api/device/restart  msg={data.get('msg','')}")
except Exception as e:
    failed += 1
    print(f"  ✗ /api/device/restart  ERROR: {e}")

try:
    resp = client.put("/api/alarm/thresholds/airTemp", json={"min": 10, "max": 40})
    data = resp.json()
    passed += 1
    print(f"  ✓ {resp.status_code} PUT /api/alarm/thresholds/airTemp  msg={data.get('msg','')}")
except Exception as e:
    failed += 1
    print(f"  ✗ PUT /api/alarm/thresholds  ERROR: {e}")

# Check greenhouse data has all fields
print("\n--- 字段完整性检查 ---")
resp = client.get("/api/greenhouse")
gh = resp.json().get("data", {})
expected_fields = ["airTemp", "airHumidity", "light", "co2", "soilMoisture",
                   "ph", "ec", "potassium", "phosphorus", "ndvi", "transpiration"]
missing = [f for f in expected_fields if f not in gh]
if not missing:
    passed += 1
    print(f"  ✓ /api/greenhouse 包含全部 {len(expected_fields)} 个字段")
else:
    failed += 1
    print(f"  ✗ /api/greenhouse 缺少字段: {missing}")

print("\n" + "=" * 60)
print(f"  结果: {passed} 通过, {failed} 失败")
print("=" * 60)
