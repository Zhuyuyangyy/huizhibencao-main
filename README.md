# 慧植本草 — 中医智慧农业平台

将中医"天人合一"理念与现代精准农业结合，通过多参数传感器实时监测、AI 本草精灵问答、节气农事指导，实现中药材种植的智能化管理。

## 系统架构

```
┌─────────────────────────────────────────────────────┐
│                   Vue 3 前端 (Vite)                  │
│  大棚监控 · 田块管理 · 本草精灵 · 产品介绍 · 联系我们  │
└──────────────────────┬──────────────────────────────┘
                       │  REST API (每 3 秒轮询)
┌──────────────────────▼──────────────────────────────┐
│                FastAPI 后端 (:8000)                  │
│  传感器数据 · 报警管理 · Excel导出 · AI对话 · 数据库   │
└──────┬──────────────────────────────┬───────────────┘
       │                              │
  ┌────▼─────┐              ┌─────────▼────────┐
  │ COS-03   │              │  DeepSeek /      │
  │ MultiGas │              │  OpenAI API      │
  │ USB HID  │              │  (本草精灵)       │
  └──────────┘              └──────────────────┘
```

## 功能模块

| 模块 | 说明 |
|------|------|
| **大棚监控** | 空气温湿度、光照、CO₂、土壤湿度、pH、EC、NPK，雷达图 + NDVI + 声谱图 |
| **田块管理** | 无棚区温湿度、CO₂、降雨、风速风向 |
| **壤博士** | 5 层 / 3 层土壤温湿度剖面、pH、EC、氮磷钾三合一 |
| **设备管理** | 通风、补光、水肥机、遮阳帘、加热、CO₂ 发生器 |
| **报警系统** | 可配置阈值，超限自动告警 |
| **历史数据** | 传感器读数持久化 + 统计查询 |
| **Excel 导出** | 定时自动导出 + 手动触发 |
| **本草精灵** | AI 中医问答，结合实时传感器数据 + 节气信息 |
| **节气轮** | 二十四节气农事指导 |

## 快速开始

### 后端

```bash
cd backend

# 创建虚拟环境（首次）
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
# → http://localhost:8000
```

### 前端

```bash
cd huiben-qianduan-main

# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev
# → http://localhost:5173
```

### USB 传感器（可选）

```bash
# 确保已关闭原厂 MultiGas.exe（设备独占）
# 安装 hidapi
pip install hidapi

# 扫描设备 VID/PID
python backend/scan_usb_devices.py

# 编辑 backend/config.py
# USB_VENDOR_ID = 0x0483
# USB_PRODUCT_ID = 0x0005
# USE_MOCK_DATA = False
```

## 项目结构

```
huizhibencao/
├── backend/
│   ├── main.py                 # FastAPI 入口 + 生命周期管理
│   ├── config.py               # 全局配置（AI、USB、导出、CORS）
│   ├── sensor_data.py          # 传感器数据（模拟 + 真实设备）
│   ├── cos03_reader.py         # COS-03 帧解析器（协议逆向）
│   ├── cos03_hid_reader.py     # HID 轮询线程（vendor command）
│   ├── usb_hid_reader.py       # 通用 USB HID 读取器
│   ├── database.py             # SQLite 持久化
│   ├── excel_export.py         # Excel 自动导出
│   ├── ai_chat.py              # AI 本草精灵对话
│   ├── scan_usb_devices.py     # USB 设备扫描工具
│   ├── requirements.txt        # Python 依赖
│   └── test_cos03_reader.py    # 帧解析器单元测试
│
├── huiben-qianduan-main/
│   ├── src/
│   │   ├── pages/              # 页面组件
│   │   │   ├── HomePage.vue    # 首页（品牌展示）
│   │   │   ├── MonitorPage.vue # 监控总览
│   │   │   ├── ProductPage.vue # 产品介绍
│   │   │   ├── HerbSpiritPage.vue # 本草精灵 AI
│   │   │   └── ContactPage.vue # 联系我们
│   │   ├── modules/
│   │   │   ├── greenhouse/     # 大棚监控模块
│   │   │   ├── openfield/      # 田块管理模块
│   │   │   ├── herbsage/       # 本草精灵模块
│   │   │   └── product/        # 产品展示模块
│   │   ├── composables/
│   │   │   ├── useSensorData.js # 传感器数据轮询
│   │   │   └── useSageAI.js    # AI 对话
│   │   ├── api/index.js        # API 请求封装
│   │   └── router/index.js     # 路由配置
│   ├── package.json
│   └── vite.config.js
│
└── software/                   # 原厂 MultiGas 软件（参考用）
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/greenhouse` | 大棚传感器数据 |
| GET | `/api/openfield` | 田块传感器数据 |
| GET | `/api/devices` | 设备列表 |
| GET | `/api/alerts` | 告警列表 |
| GET | `/api/radar` | 雷达图数据 |
| GET | `/api/snapshot` | 完整数据快照 |
| GET | `/api/soil/moisture/5layer` | 5 层土壤湿度 |
| GET | `/api/soil/ph` | 土壤 pH |
| GET | `/api/soil/ec` | 土壤电导率 |
| GET | `/api/soil/npk` | 氮磷钾 |
| GET | `/api/device/info` | 设备信息 |
| GET | `/api/alarm/thresholds` | 报警阈值 |
| PUT | `/api/alarm/thresholds/{key}` | 更新阈值 |
| GET | `/api/history` | 历史数据 |
| GET | `/api/stats` | 统计信息 |
| GET | `/api/export/excel` | 导出 Excel |
| POST | `/api/chat` | AI 本草精灵对话 |
| GET | `/api/sensor/status` | 传感器连接状态 |
| GET | `/api/health` | 健康检查 |

## 传感器协议

COS-03 MultiGas 通过 USB HID 通信，帧格式：

```
[0:3]   Header: AA 26 24
[3]     通道号 (1-11)
[5:9]   测量值 — IEEE 754 float (大端)
        若为 0，则在 [38:40] 读 uint16 大端
[14:?]  单位 (UTF-8)
[21:?]  通道名 (UTF-8)
[62:63] CRC 校验
```

通道映射：土壤湿度、土壤温度、空气湿度、pH、氮、磷、钾、叶片湿度、光照强度、CO₂、EC 电导率。

## 配置

编辑 `backend/config.py` 或创建 `backend/.env`：

```env
# AI 服务
AI_API_KEY=your-api-key
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-chat

# USB 设备
USB_VENDOR_ID=0x0483
USB_PRODUCT_ID=0x0005
USE_MOCK_DATA=False
```

## 测试

```bash
cd backend
python test_cos03_reader.py       # 帧解析器测试
python test_all_endpoints.py      # 全接口测试
```

## 技术栈

- **后端**: Python 3.12, FastAPI, Uvicorn, SQLite, APScheduler
- **前端**: Vue 3, Vite 5, TailwindCSS, ECharts, Chart.js, PixiJS
- **硬件**: COS-03 MultiGas (STMicroelectronics HID), Python hidapi
- **AI**: DeepSeek Chat / OpenAI API
