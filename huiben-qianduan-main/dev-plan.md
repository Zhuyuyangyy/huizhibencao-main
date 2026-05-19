# 慧植本草·方寸灵畦 — 前端模块化开发计划

## 一、技术架构总览

```
Tech Stack:
  Vue 3 (Composition API + <script setup>)
  Vite 5.x
  Vue Router 4
  Tailwind CSS 3.x
  Chart.js 4.x + vue-chartjs
  ECharts 6.x
  Lucide Vue Next
```

### 新增依赖
| 包名 | 用途 | 安装命令 |
|------|------|---------|
| `vue-router@4` | 页面路由 | `npm install vue-router@4` |
| `@vueuse/core` | 组合式工具 (useIntersectionObserver, useMediaQuery等) | `npm install @vueuse/core` |

### 目录结构（新增/变更）
```
huiben-qianduan/
├── public/
│   └── images/                    ← 用户生成的图片资源
│       ├── laozu-full.png
│       ├── hero-bg.webp
│       └── ...
├── src/
│   ├── main.js                    [修改] — 注册Router
│   ├── App.vue                    [重写] — 仅留 <router-view>
│   ├── style.css                  [扩展] — 新增主题变量、动画
│   ├── router/
│   │   └── index.js               [新增] — 路由配置
│   ├── layouts/
│   │   └── MainLayout.vue         [新增] — 导航栏 + 页面容器
│   ├── components/                [新增] — 可复用组件
│   │   ├── NavBar.vue             — 导航栏
│   │   ├── PanelBox.vue           — 通用数据面板框
│   │   ├── DataCard.vue           — 数据卡片
│   │   ├── StatusBadge.vue        — 状态标签
│   │   └── PageHeader.vue         — 页面标题头
│   ├── pages/
│   │   ├── HomePage.vue           — 首页
│   │   ├── MonitorPage.vue        — 在线监测
│   │   ├── ProductPage.vue        — 产品简介
│   │   ├── HerbSpiritPage.vue     — 本草精灵
│   │   └── ContactPage.vue        — 联系我们
│   ├── modules/
│   │   ├── greenhouse/            — 有棚区模块
│   │   │   ├── GreenhousePanel.vue
│   │   │   ├── RadarChart.vue
│   │   │   ├── NDVICanvas.vue
│   │   │   ├── Spectrogram.vue
│   │   │   ├── DecisionTimeline.vue
│   │   │   └── DeviceMap.vue
│   │   ├── openfield/             — 无棚区模块
│   │   │   ├── OpenFieldPanel.vue
│   │   │   ├── WeatherRadar.vue
│   │   │   ├── SoilMoistureChart.vue
│   │   │   └── DroneFeed.vue
│   │   ├── herbsage/              — 本草精灵模块
│   │   │   ├── SageCharacter.vue
│   │   │   ├── SageChat.vue
│   │   │   ├── SolarTermWheel.vue
│   │   │   └── HerbGuide.vue
│   │   └── product/               — 产品简介模块
│   │       ├── FeatureCard.vue
│   │       └── TimelineFlow.vue
│   ├── composables/               [新增] — 组合式函数
│   │   ├── useSensorData.js       — 传感器数据逻辑
│   │   ├── useSageAI.js           — 老祖AI对话逻辑
│   │   ├── useSolarTerms.js       — 节气数据
│   │   └── useDeviceControl.js    — 设备控制交互
│   └── data/                      [新增] — 静态数据
│       ├── solarTerms.js          — 二十四节气数据
│       ├── herbs.js               — 本草图鉴数据
│       └── products.js            — 产品特色数据
└── image_prompts.txt              ← 图片生成清单
```

---

## 二、路由设计

```js
// src/router/index.js
const routes = [
  { path: '/',          name: 'home',      component: () => import('@/pages/HomePage.vue') },
  { path: '/monitor',   name: 'monitor',   component: () => import('@/pages/MonitorPage.vue'),
    children: [
      { path: 'greenhouse', name: 'greenhouse', component: () => import('@/modules/greenhouse/GreenhousePanel.vue') },
      { path: 'openfield',  name: 'openfield',  component: () => import('@/modules/openfield/OpenFieldPanel.vue') },
    ]
  },
  { path: '/product',   name: 'product',   component: () => import('@/pages/ProductPage.vue') },
  { path: '/herbspirit', name: 'herbspirit', component: () => import('@/pages/HerbSpiritPage.vue') },
  { path: '/contact',   name: 'contact',   component: () => import('@/pages/ContactPage.vue') },
]
```

**路由守卫**: 无（各页面独立加载，无需鉴权）

---

## 三、页面详细设计

### P1. 首页 HomePage.vue
**目标**: 品牌展示 + 项目概览，视觉冲击力

```
┌──────────────────────────────────────────────────────┐
│ [NavBar — 固定在顶部]                                │
├──────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────── Hero Section ────────────────┐     │
│  │  背景: hero-bg.webp 全屏                      │     │
│  │  logo水印: 大号半透明 background repeat       │     │
│  │  大字: "慧植本草，方寸灵畦" (行书字体)       │     │
│  │  副标题: AI赋能道地药材，数字振兴乡土本草     │     │
│  │  装饰: 无人机/机器人/药材粒子 CSS动画漂浮     │     │
│  │  ↓ 滚动指示器                                  │     │
│  └────────────────────────────────────────────────┘     │
│                                                        │
│  ┌────────── 项目概述 Section ──────────────────┐     │
│  │  左侧: 简介文字                                │     │
│  │  右侧: 数据亮点 (3个数字: 覆盖药材数/设备数 等)│     │
│  └────────────────────────────────────────────────┘     │
│                                                        │
│  ┌────────── 核心特色 Section ──────────────────┐     │
│  │  4张feature卡片 (引用产品图片)                 │     │
│  │  鼠标悬停放大 + 发光效果                       │     │
│  └────────────────────────────────────────────────┘     │
│                                                        │
│  ┌────────── 快速入口 Section ──────────────────┐     │
│  │  3个卡片: 进入监测 → 认识老祖 → 产品详情    │     │
│  └────────────────────────────────────────────────┘     │
│                                                        │
├──────────────────────────────────────────────────────┤
│ [Footer]                                               │
└──────────────────────────────────────────────────────┘
```

**交互**:
- 药材粒子浮动 (CSS keyframes, 多个方向)
- 滚动触发渐入动画 (IntersectionObserver)
- 无人机沿弧线缓慢飞行 (CSS path animation)
- 数字滚动递增 (countUp 效果)

**所需图片**: hero-bg, logo-main, logo-watermark, drone-silhouette, robot-scout, herbal-particles, pattern-decoration

---

### P2. 在线监测 MonitorPage.vue
**目标**: 重构现有大屏 + 增加交互深度

```
┌──────────────────────────────────────────────────────────┐
│ [NavBar]                                                │
├──────────────────────────────────────────────────────────┤
│  ┌── 监测模式切换 ──────────────────────────────────┐  │
│  │  [🌿 有棚区] ║ [🌾 无棚区]   — 分页切换按钮     │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  === 有棚区视图 (GreenhousePanel.vue) ===                │
│  ┌────┬──────────────────┬────┐                          │
│  │ 左 │      中          │ 右 │                          │
│  │    │                   │    │                          │
│  │ 八维雷达图 (可点击     │ 植 │                          │
│  │ →展开详情浮窗)        │ 物 │                          │
│  │    │  大棚标注示意图   │ 生 │                          │
│  │ 环境数据卡片           │    │ 理 │                     │
│  │ (点击→历史趋势图)     │ 每个设备是                     │
│  │                       │ 热区,点击弹    │ 多 │          │
│  │ 实时数值              │ 出设备详情      │ 光 │          │
│  │ (温/湿/CO₂/光照)      │ 浮窗:           │ 谱 │          │
│  │                       │ 状态/数据/控制   │    │         │
│  │                       │ 按钮(开/关/调节) │ │    │       │
│  │ ─── ─── ───          │                   │    │        │
│  │ [新增]告警列表         │ ─── ─── ───      │ 视听融合    │
│  │ 点击→弹出处理建议     │ [新增]时间穿梭轴  │ 病虫害预警  │
│  │                      │ 拖拽查看历史数据  │            │
│  │                      │                   │ AI决策日志  │
│  │                      │                   │ (可点击展开) │
│  └────┴──────────────────┴────┘                          │
│                                                          │
│  === 无棚区视图 (OpenFieldPanel.vue) ===                 │
│  ┌──────┬──────────┬──────┐                              │
│  │ 左   │   中      │ 右   │                              │
│  │      │           │      │                              │
│  │ 环境监测          │ AI   │                              │
│  │ (气象雷达/        │ 病虫害                              │
│  │  温湿度/预报)     │ 预警                               │
│  │      │ 统计数据区 │ (可点                              │
│  │ 土壤水分   │ 无人机视频  │ 击→详情)                      │
│  │ 多层展示   │ 可点击切换视角 │      │                     │
│  │ (ECharts)  │           │ 多光谱                           │
│  │            │ 底部功能按钮 │ 无人机图                      │
│  │ 土壤养分   │ (全局视角/   │ [新增]点击                     │
│  │ (可点击    │  生长模型/   │ 可放大查看                    │
│  │  展开详情) │  网格管理等) │                               │
│  │            │ [新增]每个   │                               │
│  │            │ 按钮展开     │                               │
│  │            │ 对应面板     │                               │
│  └──────┴──────────┴──────┘                              │
└──────────────────────────────────────────────────────────┘
```

**改进增量（用户最关心的"可点击"）**:

| 改进项 | 实现方式 | 交互反馈 |
|--------|---------|---------|
| 设备热区点击 | 在SVG标注图上叠加透明click区域 | 弹出浮窗: 设备名/状态/数据/控制按钮 |
| 数据卡片点击展开 | 每个DataCard绑定click | 展开为半屏趋势图 (ECharts/Chart.js) |
| 无人机视角切换 | 点击视频区域弹出多视角选择 | 切换视频源或图片 |
| 告警可操作 | 告警条目绑定click | 弹出处理建议 + "一键执行"按钮 |
| 时间穿梭 | 底部时间轴滑块 | 拖动时全局数据回滚到对应时间点 |
| 功能按钮穿透 | 底部按钮点击展开对应面板 | 右侧滑出或弹窗 |

**状态管理 (useSensorData composable)**:
```js
// 当前传感器数据
const sensorData = ref({ ... })
// 历史数据回放状态
const playbackTime = ref(null)
const isPlayback = computed(...)
// 选中的设备/卡片
const selectedDevice = ref(null)
```

**所需图片**: 沿用现有 public/ 资源，新增无

---

### P3. 产品简介 ProductPage.vue
**目标**: 图文并茂展示项目四大特色

```
┌──────────────────────────────────────────────────────┐
│ [NavBar]                                             │
├──────────────────────────────────────────────────────┤
│  ┌────────── Hero Banner ───────────────────────┐    │
│  │  背景: product-hero.webp                     │    │
│  │  叠加: "AI赋能中草药全产业链智慧化解决方案"   │    │
│  └──────────────────────────────────────────────┘    │
│                                                        │
│  ┌────────── 项目概述 ────────────────────────┐      │
│  │  左侧: 简介文字 (引用报告书内容)            │      │
│  │  右侧: 核心数据 (覆盖品种/种植面积/等)      │      │
│  └──────────────────────────────────────────────┘      │
│                                                        │
│  ┌────────── "种管没收" 流程展示 ──────────────┐      │
│  │  水平循环时间轴                              │      │
│  │  种 → 管 → 护 → 收  (每个阶段可点击展开)    │      │
│  │  展开显示: 描述 + 数据 + 配图                │      │
│  └──────────────────────────────────────────────┘      │
│                                                        │
│  ┌────────── 四大特色 ─────────────────────────┐      │
│  │  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   │      │
│  │  │全流程化│  │数据驱动│  │精准智能│  │绿色高效│   │      │
│  │  │ 配图  │  │ 配图  │  │ 配图  │  │ 配图  │   │      │
│  │  │feature│  │feature│  │feature│  │feature│   │      │
│  │  │ -full  │  │-data  │  │-prec  │  │-green │   │      │
│  │  └──────┘  └──────┘  └──────┘  └──────┘   │      │
│  └──────────────────────────────────────────────┘      │
│                                                        │
│  ┌────────── 文旅融合 ─────────────────────────┐      │
│  │  展示文旅板块内容 (报告书文旅部分)            │      │
│  └──────────────────────────────────────────────┘      │
│                                                        │
├──────────────────────────────────────────────────────┤
│ [Footer]                                               │
└──────────────────────────────────────────────────────┘
```

**交互**: 点击"种管没收"各阶段展开详情; 特色卡片hover放大

**所需图片**: product-hero, feature-full-process, feature-data-driven, feature-precision-ai, feature-green-eco

---

### P4. 本草精灵 HerbSpiritPage.vue
**目标**: 老祖智能体交互核心页面

```
┌────────────────────────────────────────────────────────────┐
│ [NavBar]                                                   │
├────────────────────────────────────────────────────────────┤
│ ┌── 左侧区域 (65%) ─────────┬── 右侧区域 (35%) ───────┐   │
│ │                           │                           │   │
│ │  ┌── 老祖对话区 ──────┐  │  ┌── 老祖形象 ──────┐    │   │
│ │  │  聊天消息流          │  │  │  laozu-full.png   │   │   │
│ │  │  老祖消息(头像+气泡)│  │  │  表情会随对话变化 │   │   │
│ │  │  用户消息(右对齐)    │  │  │  叶子微微飘动    │   │   │
│ │  │                       │  │  │  (CSS动画)       │   │   │
│ │  │  ┌─── 快捷提问 ──┐   │  │  │                   │   │   │
│ │  │  │ [当前湿度高怎么办]│  │  │  └──────────────────┘   │   │
│ │  │  │ [今日养生建议]    │  │  │                           │   │
│ │  │  │ [讲讲三七功效]   │  │  │  ┌── 当前状态 ──────┐    │   │
│ │  │  └─────────────────┘   │  │  │  节气: 立夏       │   │   │
│ │  │                        │  │  │  天气: 晴 26°C    │   │   │
│ │  │  ┌── 输入区 ───────┐  │  │  │  棚内温度: 28°C   │   │   │
│ │  │  │ [输入...]🎙️ ➤  │  │  │  棚内湿度: 65%     │   │   │
│ │  │  └─────────────────┘  │  │  └──────────────────┘   │   │
│ │  └───────────────────────┘  │                           │   │
│ │                              │  ┌── 快速功能 ──────┐    │   │
│ │                              │  │  🍃 节气轮盘      │   │   │
│ │                              │  │  📖 本草图鉴      │   │   │
│ │                              │  │  🔊 语音开关      │   │   │
│ │                              │  │  🔔 实时告警      │   │   │
│ │                              │  └──────────────────┘   │   │
│ └──────────────────────────────┴──────────────────────────┘   │
│                                                              │
│ ┌── Tab切换: [🍃节气轮盘] [📖本草图鉴] [🔔告警] ─────┐     │
│ │                                                          │     │
│ │  Tab=节气轮盘:                                          │     │
│ │  ┌────────────────────────────────────────┐              │     │
│ │  │  🌞 二十四节气轮盘 (SolarTermWheel)    │              │     │
│ │  │  圆环布局, 当前节气高亮                  │              │     │
│ │  │  点击→ 显示:                            │              │     │
│ │  │  节气名 + 日期 + 养生建议 + 农事建议     │              │     │
│ │  │  + 推荐药材 + 背景切换季节色             │              │     │
│ │  └────────────────────────────────────────┘              │     │
│ │                                                          │     │
│ │  Tab=本草图鉴:                                          │     │
│ │  ┌────────────────────────────────────────┐              │     │
│ │  │  药材网格 (HerbGuide)                   │              │     │
│ │  │  顶部筛选: 四气 | 五味 | 归经           │              │     │
│ │  │  卡片: 图 + 名 + 性味 → 点击展开详情    │              │     │
│ │  │  详情: 大图 + 功效 + 用法 + 配伍禁忌    │              │     │
│ │  └────────────────────────────────────────┘              │     │
│ │                                                          │     │
│ │  Tab=告警: 见P2告警列表                                  │     │
│ └──────────────────────────────────────────────────────────┘     │
├──────────────────────────────────────────────────────────────────┤
│ [Footer]                                                         │
└──────────────────────────────────────────────────────────────────┘
```

**老祖 AI 智能体 (useSageAI.js)**:

```js
// 核心设计
const sageAI = {
  // 状态
  messages: ref([]),
  isTyping: ref(false),
  currentExpression: ref('happy'), // happy | think | surprise | worry
  
  // 能力
  async askQuestion(question) { /* 调用AI API */ },
  getInterventionAdvice(sensorData) { /* 根据实时数据生成建议 */ },
  getHealthTip(currentSolarTerm) { /* 节气养生 */ },
  getHerbKnowledge(herbName) { /* 本草科普 */ },
  
  // AI API 对接方案 (二选一)
  // Option A: 直接调用大模型API (需后端代理或前端API key)
  // Option B: 预设规则 + 前端内置知识库 (不依赖网络)
  
  // 建议: 先用Option B做Mock, 后期对接Option A
}
```

**对话系统消息结构**:
```js
{
  id: 'msg_001',
  role: 'sage' | 'user',
  content: '棚内湿度偏高，老身建议开启通风~',
  type: 'text' | 'herb_card' | 'alert' | 'suggestion',
  timestamp: Date.now(),
  metadata: { /* 关联数据 */ }
}
```

**语音 (TTS)**:
- 使用 Web Speech API (`window.speechSynthesis`)
- 选择中文语音 (zh-CN)
- 老祖说话时同步播放
- 可开关

**所需图片**: laozu-full, laozu-portrait, laozu-expressions, laozu-hologram, solar-term-wheel, season-spring~winter, herb-* ×8

---

### P5. 联系我们 ContactPage.vue
**目标**: 简洁联系方式

```
┌──────────────────────────────────────────────────────┐
│ [NavBar]                                             │
├──────────────────────────────────────────────────────┤
│  ┌────────── Hero ────────────────────────────┐      │
│  │  背景: contact-bg.webp                    │      │
│  │  标题: 联系我们                            │      │
│  └────────────────────────────────────────────┘      │
│                                                        │
│  ┌──── 信息 ────┬──── 留言表单 ─────────────┐         │
│  │ 地址: ...    │  姓名 / 邮箱 / 电话 / 留言 │         │
│  │ 电话: ...    │  [发送]                     │         │
│  │ 邮箱: ...    │                             │         │
│  │ 公众号二维码 |                             │         │
│  └──────────────┴────────────────────────────┘         │
│                                                        │
├──────────────────────────────────────────────────────┤
│ [Footer]                                               │
└──────────────────────────────────────────────────────┘
```

**所需图片**: contact-bg

---

## 四、全局样式主题系统

```css
/* style.css — 扩展主题变量 */
:root {
  /* === 主色调 (东方科技禅意) === */
  --color-bg-base: #050d14;        /* 深墨底色 */
  --color-bg-panel: rgba(15, 35, 45, 0.85);  /* 面板底 */
  --color-jade: #2d8a6e;           /* 翡翠绿 - 主色 */
  --color-jade-light: #4ecdc4;     /* 青绿 - 发光 */
  --color-gold: #c4a86a;           /* 琥珀金 - 点缀 */
  --color-herb: #6b9f6b;           /* 艾草绿 - 柔和过渡 */
  --color-ink: #1a1a2e;            /* 墨色 */
  --color-paper: #f5e6d3;          /* 宣纸白 */
  --color-cyan-glow: #00ffcc;      /* 青发光 - 保留 */
  
  /* === 字体 === */
  --font-display: 'Noto Serif SC', 'STSong', serif;
  --font-body: 'Noto Sans SC', sans-serif;
  --font-number: 'Oswald', sans-serif;
}
```

---

## 五、开发阶段与顺序

### Phase 0 — 项目基础设施 (1h)
- [ ] 安装 vue-router@4
- [ ] 创建 router/index.js
- [ ] 重写 App.vue → `<router-view>`
- [ ] 创建 layouts/MainLayout.vue
- [ ] 创建 theme.css (全局主题变量)
- [ ] 验证: 空页面路由正常

### Phase 1 — 导航栏 + 公共组件 (2h)
- [ ] 实现 NavBar.vue (5个导航项, 路由激活状态, 毛玻璃效果)
- [ ] 实现 PanelBox.vue (通用面板容器, 复用现有四角边框)
- [ ] 实现 DataCard.vue (数据卡片, 支持点击展开)
- [ ] 实现 PageHeader.vue (页面标题)
- [ ] 实现 Footer

### Phase 2 — 首页 (3h)
- [ ] Hero Section: 背景图 + logo水印 + 大字 + 副标题
- [ ] 装饰动画: 无人机 / 机器人 / 药材粒子 CSS动画
- [ ] 项目概述 Section + 数据亮点 (scroll-triggered 数字动画)
- [ ] 核心特色 Section (4张feature卡片, hover效果)
- [ ] 快速入口 Section (跳转到其他页面的卡片)
- [ ] 页面加载动画 (staggered reveal)

### Phase 3 — 在线监测 (4h)
- [ ] 提取: RadarChart.vue (从App.vue拆出)
- [ ] 提取: NDVICanvas.vue (从App.vue拆出)
- [ ] 提取: Spectrogram.vue (从App.vue拆出)
- [ ] 提取: DecisionTimeline.vue (从App.vue拆出)
- [ ] 提取: DeviceMap.vue (从App.vue拆出设备标注 + SVG线)
- [ ] 提取: OpenFieldPanel.vue (无棚区全组件)
- [ ] 新增: 设备热区点击 → 详情浮窗
- [ ] 新增: 数据卡片点击 → 趋势展开
- [ ] 新增: 时间穿梭轴
- [ ] 新增: 告警可操作 (建议 + 一键执行)

### Phase 4 — 产品简介 (2h)
- [ ] Hero Banner
- [ ] 项目概述区
- [ ] "种管没收" 流程时间轴 (点击展开)
- [ ] 四大特色卡片 (引入生成图片)
- [ ] 文旅融合板块

### Phase 5 — 本草精灵 (4h)
- [ ] 老祖形象组件 (表情切换, 叶子飘动CSS)
- [ ] 对话界面 (消息流, 输入框, 快捷提问)
- [ ] useSageAI composable (对话逻辑 + Mock接口)
- [ ] 实时状态区 (节气/天气/棚内数据)
- [ ] 二十四节气轮盘 (环形布局, 点击详情)
- [ ] 本草图鉴 (药材网格 + 筛选 + 详情弹窗)
- [ ] TTS语音播放 (Web Speech API)
- [ ] 告警集成

### Phase 6 — 联系我们 (1h)
- [ ] Hero区
- [ ] 联系信息
- [ ] 留言表单 (前端验证)
- [ ] 底部Footer

### Phase 7 — 集成与打磨 (2h)
- [ ] 全局动画统一 (转场动画, 滚动触发)
- [ ] 图片资源引入与优化
- [ ] 响应式检查 (大屏为主, 基础中屏适配)
- [ ] 性能优化 (组件懒加载, 图片懒加载)
- [ ] 浏览器兼容性

---

## 六、数据模型

### 二十四节气数据结构 (solarTerms.js)
```js
{
  id: 1,
  name: '立春',
  englishName: 'Start of Spring',
  date: '2月3-5日',
  element: '木',
  description: '...',
  healthTip: '疏肝理气，宜食辛甘...',
  farmingTip: '开始育苗，注意防虫...',
  recommendedHerbs: ['薄荷', '菊花'],
  seasonBg: 'season-spring.webp',
  icon: '🌱'
}
```

### 本草图鉴数据结构 (herbs.js)
```js
{
  id: 'ginseng',
  name: '人参',
  latinName: 'Panax ginseng',
  image: 'herb-ginseng.png',
  nature: '温',         // 四气: 寒热温凉
  flavor: ['甘', '微苦'], // 五味
  meridian: ['脾', '肺', '心'], // 归经
  efficacy: '大补元气，复脉固脱...',
  usage: '煎服，3-9g...',
  caution: '不宜与藜芦同用...',
  description: '多年生草本植物...',
  category: '补气药'
}
```

### 传感器数据结构 (useSensorData.js)
```js
{
  greenhouse: {
    light: 15800,        // 光照 lux
    ph: 6.38,            // pH值
    soilMoisture: 32.6,  // 土壤湿度 %
    co2: 613,            // CO₂浓度 ppm
    airHumidity: 68.2,   // 空气湿度 %
    airTemp: 26.4,       // 空气温度 °C
    potassium: 28.6,     // 钾 % 
    phosphorus: 192,     // 磷 mg/kg
    ndvi: 0.72,          // NDVI指数
    transpiration: 4.5,  // 蒸腾速率
    ec: 1.2,             // 电导率
  },
  devices: [
    { id: 'fan', name: '通风系统', status: 'on', value: 65 },
    { id: 'light', name: 'LED补光灯', status: 'on', value: 60 },
    { id: 'water', name: '智能水肥机', status: 'running', value: 28 },
    // ...
  ],
  alerts: [
    { id: 1, type: 'pest', message: '钻心虫声学信号增强', time: '14:34:42', severity: 'warning' },
  ]
}
```

---

## 七、图片资源集成计划

用户生成的图片放到 `public/images/` 后，组件中这样引用:

```vue
<img src="/images/laozu-full.png" alt="老祖" />
<!-- 或动态绑定 -->
<img :src="`/images/${herb.image}`" :alt="herb.name" />
```

**需要用户优先生成的图片** (按依赖顺序):
1. `laozu-full.png` + `laozu-portrait.png` — 老祖组件依赖
2. `hero-bg.webp` — 首页依赖
3. `logo-main.png` + `logo-watermark.png` — 首页 + NavBar依赖
4. `product-hero.webp` + 4张feature卡 — 产品简介依赖
5. `solar-term-wheel.webp` + 四季背景 — 节气轮盘依赖
6. `herb-*.png` ×8 — 本草图鉴依赖
7. `drone-silhouette.webp` + `robot-scout.webp` + `herbal-particles.webp` — 首页装饰
8. `laozu-hologram.png` + `laozu-expressions.png` — 老祖补充
9. `contact-bg.webp` — 联系我们
10. `pattern-decoration.webp` + `wuqinxi-animation.webp` — 装饰

---

## 八、风险与应对

| 风险 | 影响 | 应对 |
|------|------|------|
| App.vue 1504行拆组件工作量大 | Phase 3耗时可能超预期 | 先拆出独立功能模块，复用原有逻辑不动 |
| 老祖AI对话需后端API | 功能受限 | Phase 5先用Mock数据 + 前端知识库，后期对接API |
| 大量图片加载慢 | 首页首屏性能 | 图片使用WebP格式，poster占位，懒加载 |
| 无棚区视频 ~5MB | 加载延迟 | 视频使用preload="none"，点击加载 |
| 用户生成图片风格不一致 | 视觉不统一 | 使用同样的提示词前缀保证风格连贯 |

---

## 九、AI图片批量生成进度

### 生成工具
- **API**: MiniMax image-01 (https://api.minimaxi.com/v1/image_generation)
- **脚本**: `D:\work\workm\hulianwang+-huizhibencao\v3\batch_generate_images.py`
- **输出目录**: `D:\work\workm\hulianwang+-huizhibencao\v3\huiben-qianduan\public`
- **提示词源**: `D:\work\workm\hulianwang+-huizhibencao\v3\image_prompts.txt`

### 当前进度 （2026-05-15）

| 分组 | 总计 | 已完成 | 待生成 |
|------|------|--------|--------|
| GROUP 1 - 首页 Hero & 背景 | 6 | 6 | 0 |
| GROUP 2 - 产品简介 Feature Cards | 5 | 5 | 0 |
| GROUP 3 - 老祖角色 | 4 | 4 | 0 |
| GROUP 4 - 二十四节气轮盘 | 5 | 5 | 0 |
| GROUP 5 - 本草图鉴 | 8 | 8 | 0 |
| GROUP 6 - 其他装饰元素 | 3 | 0 | 3 |
| **合计** | **31** | **28** | **3** |

### 待生成图片（GROUP 6）

**6.1 contact-bg.webp** — 联系我们页面背景
- 尺寸: 1920×1080px | 格式: WebP | 比例: 16:9
- Prompt:
  ```
  A welcoming entrance to a modern traditional Chinese medicine garden. A elegant wooden archway with curved traditional roof stands at the entrance, flanked by lush bamboo groves. A stone path leads into the garden. The building beyond blends traditional Chinese architecture (white walls, grey tiles) with modern glass greenhouse elements. Golden hour sunset lighting creates warm welcoming atmosphere. Purple and lavender plants line the path. Peaceful, inviting. Style: architectural photography, premium resort aesthetic. --ar 16:9 --v 6
  ```

**6.2 pattern-decoration.webp** — 装饰纹理（页面底纹）
- 尺寸: 800×800px | 格式: WebP | 比例: 1:1
- Prompt:
  ```
  A seamless repeating pattern combining traditional Chinese cloud patterns (祥云) with subtle circuit board traces and herbal leaf silhouettes. Very faint, like a watermark on dark background. Monochromatic in very dark jade green on near-black background. Suitable as a subtle page background texture for a technology-meets-traditional-Chinese-medicine website. Elegant, understated. --ar 1:1 --v 6
  ```

**6.3 wuqinxi-animation.webp** — 五禽戏线条动画参考图
- 尺寸: 600×600px | 格式: WebP | 比例: 1:1
- Prompt:
  ```
  Minimalist line art of a person performing the "Five Animals Exercise" (五禽戏) — the Tiger pose (虎戏): a figure in a wide powerful stance, arms extended like tiger claws, dynamic flowing movement captured in elegant continuous single-line drawing style. White lines on dark background. Traditional Chinese ink brush stroke quality meets minimalist vector art. Suitable for animation reference. --ar 1:1 --v 6
  ```

### 继续生成方法

额度刷新后运行:
```bash
cd D:\work\workm\hulianwang+-huizhibencao\v3
PYTHONIOENCODING=utf-8 python -u batch_generate_images.py
```

脚本会自动解析 `image_prompts.txt`，调用 MiniMax API（model: image-01）生成图片，并用 Pillow 转换为目标格式（PNG/WebP）保存到 `public/` 目录。
