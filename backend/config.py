import os
from pathlib import Path


def _load_project_env() -> dict:
    """Load simple KEY=VALUE pairs from backend/.env with project-level precedence."""
    env_path = Path(__file__).with_name(".env")
    values = {}

    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value

    return values


_PROJECT_ENV = _load_project_env()


def _get_setting(name: str, default: str = "") -> str:
    if name in _PROJECT_ENV:
        return _PROJECT_ENV[name]
    return os.getenv(name, default)


def _get_project_setting(name: str, default: str = "") -> str:
    return _PROJECT_ENV.get(name, default)


# === DeepSeek AI ===
DEEPSEEK_API_KEY = _get_project_setting("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_BASE_URL = _get_project_setting("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1").rstrip("/")
DEEPSEEK_MODEL = _get_project_setting("DEEPSEEK_MODEL", "deepseek-chat").strip()
OPENAI_API_KEY = _get_project_setting("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = _get_project_setting("OPENAI_BASE_URL", "").strip().rstrip("/")
OPENAI_MODEL = _get_project_setting("OPENAI_MODEL", "").strip()

# === Generic AI (sourced only from backend/.env, with DeepSeek fallback) ===
AI_API_KEY = _get_project_setting("AI_API_KEY", "").strip() or OPENAI_API_KEY or DEEPSEEK_API_KEY
AI_BASE_URL = _get_project_setting("AI_BASE_URL", "").strip().rstrip("/") or OPENAI_BASE_URL or DEEPSEEK_BASE_URL
AI_MODEL = _get_project_setting("AI_MODEL", "").strip() or OPENAI_MODEL or DEEPSEEK_MODEL

_PROVIDER_LABEL = _get_project_setting("AI_PROVIDER_LABEL", "").strip()
if _PROVIDER_LABEL:
    AI_PROVIDER_LABEL = _PROVIDER_LABEL
elif "openai" in AI_BASE_URL.lower():
    AI_PROVIDER_LABEL = "OpenAI"
elif "deepseek" in AI_BASE_URL.lower() or AI_MODEL.lower().startswith("deepseek"):
    AI_PROVIDER_LABEL = "DeepSeek"
else:
    AI_PROVIDER_LABEL = "AI"

# === Excel Export ===
EXCEL_EXPORT_INTERVAL_MINUTES = 10
EXCEL_EXPORT_DIR = os.path.join(os.path.dirname(__file__), "exports")

# === USB HID Device — COS-03 MultiGas ===
USB_VENDOR_ID = 0x0483       # STMicroelectronics (vendor of MultiGas sensor)
USB_PRODUCT_ID = 0x0005      # COS-03 MultiGas HID device
USB_DATA_FORMAT = "cos03"    # COS-03 vendor protocol (AA 26 24 header)
USB_READ_INTERVAL = 3        # 读取间隔(秒) — matches frontend 3s poll

# === Sensor Data Mode ===
# True = 使用模拟数据 (开发测试)
# False = 使用USB HID真实数据
USE_MOCK_DATA = True

# === CORS ===
CORS_ORIGINS = [
    "http://localhost:5173",   # Vite dev server
    "http://localhost:5174",   # Vite dev server (alternate port)
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
    "http://localhost:4173",   # Vite preview
]
