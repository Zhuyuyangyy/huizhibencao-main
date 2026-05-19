# 慧种仁心 - AI智能农业决策平台

基于 Vue 3 + Vite 构建的现代化智慧农业可视化决策平台。

## 功能特性

### 🏠 有棚区监控
- **天地环境监控**：实时监测光照、pH值、土壤湿度、CO₂浓度、空气温湿度等环境指标
- **植物生理与多光谱数据**：NDVI热力图展示、蒸腾速率分析
- **视听融合病虫害预警**：基于声学信号的病虫害识别与预警系统
- **AI决策与控制指令流**：实时展示AI系统的决策日志和控制指令

### 🌾 无棚区监控
- **环境监测**：气象雷达数据、温度、湿度、降水概率等
- **土壤墒情监测**：多层土壤湿度数据可视化（10cm/20cm/40cm/60cm）
- **土壤养分检测**：有机质、氮、磷、钾等养分指标
- **无人机巡检**：无人机实时巡检视频监控

## 技术栈

- **前端框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5.x
- **样式方案**: Tailwind CSS 3.x
- **图表库**: Chart.js + vue-chartjs、ECharts
- **图标库**: Lucide Vue Next、Phosphor Icons
- **动画效果**: Canvas 2D、CSS Animations

## 项目结构

```
├── public/                    # 静态资源
│   ├── chongzi.png           # 虫子图标
│   ├── hui-background1.jpg   # 背景图
│   ├── leidaditu.png         # 雷达地图
│   ├── wupeng.mp4            # 无人机视频
│   └── wurenji.png           # 无人机图片
├── src/
│   ├── App.vue               # 主应用组件
│   ├── main.js               # 应用入口
│   └── style.css             # 全局样式
├── index.html                # HTML模板
├── package.json              # 项目依赖
├── vite.config.js            # Vite配置
├── tailwind.config.js        # Tailwind配置
└── postcss.config.js         # PostCSS配置
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

启动后访问 `http://localhost:5173`

### 生产构建

```bash
npm run build
```

### 预览构建结果

```bash
npm run preview
```

## 核心功能模块

### 环境监测仪表盘
- 八维雷达图展示环境指标
- 实时数值卡片显示关键数据
- 动态更新时间戳

### 多光谱数据分析
- NDVI植被指数热力图
- 蒸腾速率折线图
- 实时数据趋势分析

### 病虫害预警系统
- 声学频谱实时分析
- 病虫害类型识别（钻心虫、根结线虫等）
- 置信度分级显示

### AI决策日志
- 时间线展示决策记录
- 状态标识（执行中/已完成/告警）
- 支持展开查看更多

## 特色亮点

1. **科幻风格UI设计**：采用青色科技主题，配合动态光效和动画
2. **实时数据可视化**：多种图表类型展示农业数据
3. **交互式控制面板**：支持有棚区/无棚区切换
4. **响应式布局**：适配不同屏幕尺寸

## 许可证

MIT License
