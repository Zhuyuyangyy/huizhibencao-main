"""
Quick diagnostic script to test if the backend can start correctly.
Run this to check for import errors or configuration issues.
"""
import sys
import os

print("=" * 50)
print("  慧植本草 后端诊断工具")
print("=" * 50)
print()

# Check Python version
print(f"[1] Python版本: {sys.version}")
print(f"[2] 工作目录: {os.getcwd()}")
print()

# Test imports one by one
modules = [
    ("config", "配置文件"),
    ("database", "数据库模块"),
    ("sensor_data", "传感器数据"),
    ("ai_chat", "AI对话模块"),
    ("excel_export", "Excel导出"),
]

all_ok = True
for module_name, desc in modules:
    try:
        __import__(module_name)
        print(f"  [OK] {desc} ({module_name})")
    except Exception as e:
        print(f"  [FAIL] {desc} ({module_name}): {e}")
        all_ok = False

print()

# Test FastAPI app
try:
    from main import app
    print("[OK] FastAPI应用导入成功")
except Exception as e:
    print(f"[FAIL] FastAPI应用导入失败: {e}")
    all_ok = False

print()

if all_ok:
    print("=" * 50)
    print("  所有模块导入正常！可以启动服务器。")
    print("=" * 50)
    print()
    print("启动命令:")
    print("  python main.py")
    print()
    print("测试API:")
    print("  浏览器访问: http://localhost:8000/docs")
    print("  健康检查: http://localhost:8000/api/health")
else:
    print("=" * 50)
    print("  发现错误！请检查上面的 [FAIL] 项目。")
    print("=" * 50)
    print()
    print("常见解决方法:")
    print("  1. 确保在 backend 目录下运行此脚本")
    print("  2. 安装依赖: pip install -r requirements.txt --break-system-packages")
    print("  3. 检查 Python 版本是否为 3.8+")

input("\n按回车键退出...")
