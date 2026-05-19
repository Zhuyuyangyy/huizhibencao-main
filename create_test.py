import os

content = r"""@echo off
echo === API Test ===
echo.
echo [1] Health
curl -s http://localhost:8000/api/health
echo.
echo.
echo [2] Sensor Data
curl -s http://localhost:8000/api/greenhouse
echo.
echo.
echo [3] AI Chat
curl -s -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"question\": \"hello\", \"withContext\": false}"
echo.
echo.
echo === Done ===
pause
"""

path = os.path.join(os.path.dirname(__file__), "test_api.bat")
with open(path, "w", encoding="ascii") as f:
    f.write(content)
print(f"Created: {path}")
