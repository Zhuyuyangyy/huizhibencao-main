@echo off
chcp 65001 >nul
echo ============================================
echo   CORS 连通性测试
echo ============================================
echo.

echo [1] 测试后端是否在运行...
curl -s http://localhost:8000/api/health
if %errorlevel% neq 0 (
    echo.
    echo [错误] 后端服务未运行或无法连接！
    echo.
    echo 解决方法:
    echo   1. 先关闭所有 Python 窗口
    echo   2. 进入 backend 目录
    echo   3. 运行: python main.py
    echo.
    goto :end
)
echo.
echo [OK] 后端服务正在运行！
echo.

echo [2] 测试 CORS 预检请求...
curl -s -I -X OPTIONS http://localhost:8000/api/greenhouse -H "Origin: http://localhost:5173" -H "Access-Control-Request-Method: GET"
echo.

echo [3] 测试 API 数据接口...
curl -s http://localhost:8000/api/greenhouse
echo.
echo.

echo [4] 测试 AI 对话接口...
curl -s -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"question\": \"你好\", \"withContext\": false}"
echo.
echo.

echo ============================================
echo   测试完成！
echo ============================================
echo.
echo 如果 CORS 仍有问题，请尝试:
echo   1. 关闭所有浏览器标签页
echo   2. 清除浏览器缓存 (Ctrl+Shift+Delete)
echo   3. 重新打开浏览器访问前端

:end
echo.
pause
