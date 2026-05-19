<template>
  <div class="flex flex-col h-full">
    <!-- 3-Column Grid -->
    <div class="grid grid-cols-[3fr_5fr_3fr] gap-4 flex-1 overflow-hidden" style="min-height: 0;">
      <!-- ========== LEFT COLUMN ========== -->
      <div class="flex flex-col gap-4 overflow-y-auto custom-scrollbar pr-1 h-full">
        <PanelBox title="天 / 地环境监控" subtitle="实时">
          <div class="h-[220px]">
            <RadarChart />
          </div>
          <div class="grid grid-cols-4 gap-2 mt-3">
            <div v-for="(item, idx) in envMonitors" :key="idx"
                 class="bg-gradient-to-br from-[#002b4d]/60 to-[#001a2e]/80 p-2.5 rounded-lg border border-[var(--color-border)] flex flex-col items-center justify-center hover:border-[var(--color-border-strong)] transition-all duration-300 hover:shadow-[0_0_15px_rgba(0,255,255,0.2)]">
              <component :is="item.icon" :size="16" class="text-[var(--color-cyan-glow)] mb-1.5" />
              <span class="text-[10px] text-gray-400 mb-0.5">{{ item.label }}</span>
              <div class="flex items-baseline gap-1">
                <span class="text-lg font-bold text-white">{{ item.val }}</span>
                <span class="text-[10px] text-gray-400">{{ item.unit }}</span>
              </div>
            </div>
          </div>
        </PanelBox>
        <PanelBox title="植物生理与多光谱数据" subtitle="14:35:20" class="flex-1">
          <div class="mb-3">
            <div class="text-xs text-gray-400 mb-2">NDVI 热力图</div>
            <NDVICanvas />
          </div>
          <div class="flex-1 flex flex-col">
            <div class="text-xs text-gray-400 mb-1">蒸腾速率 (mmol/m²/s)</div>
            <div class="w-full relative" style="min-height: 100px;">
              <Line :data="lineChartData" :options="lineChartOptions" />
            </div>
          </div>
        </PanelBox>
      </div>

      <!-- ========== CENTER COLUMN ========== -->
      <div class="relative w-full h-full rounded-xl overflow-hidden">
        <div class="absolute inset-0">
          <div class="absolute top-[15%] left-[25%]">
            <svg class="absolute w-16 h-8 pointer-events-none" style="transform: rotate(180deg); top: -40px; left: -20px;" viewBox="0 0 64 32">
              <line x1="0" y1="16" x2="60" y2="16" stroke="#00ffff" stroke-width="1" stroke-dasharray="2,2" />
            </svg>
            <div class="label-clickable" @click="onDeviceLabelClick('drone')">多光谱无人机</div>
          </div>
          <div class="absolute bottom-[20%] left-[20%]">
            <svg class="absolute -right-6 top-1/2 -translate-y-1/2 w-12 h-8 pointer-events-none" viewBox="0 0 48 32">
              <line x1="0" y1="16" x2="40" y2="16" stroke="#00ffff" stroke-width="1" stroke-dasharray="2,2" />
            </svg>
            <div class="label-clickable" style="animation-delay: 0.2s;" @click="onDeviceLabelClick('robot')">巡检机器人</div>
          </div>
          <div class="absolute top-[35%] left-[52%]">
            <svg class="absolute left-1/2 -translate-x-1/2 w-8 h-12 pointer-events-none" style="top: -120px;" viewBox="0 0 32 48">
              <line x1="16" y1="0" x2="16" y2="40" stroke="#00ffff" stroke-width="1" stroke-dasharray="2,2" />
            </svg>
            <div class="label-clickable" style="animation-delay: 0.4s; left: -37px; top: -150px;" @click="onDeviceLabelClick('fan')">通风系统</div>
          </div>
          <div class="absolute top-[38%] left-[65%]">
            <svg class="absolute left-1/2 -translate-x-1/2 w-8 h-12 pointer-events-none" style="top: 23px;" viewBox="0 0 32 48">
              <line x1="16" y1="0" x2="16" y2="40" stroke="#00ffff" stroke-width="1" stroke-dasharray="2,2" />
            </svg>
            <div class="label-clickable" style="animation-delay: 0.6s;" @click="onDeviceLabelClick('light')">LED补光灯</div>
          </div>
          <div class="absolute top-[50%] right-[15%]">
            <svg class="absolute top-1/2 -translate-y-1/2 w-16 h-8 pointer-events-none" style="left: 70px;" viewBox="0 0 64 32">
              <line x1="64" y1="16" x2="8" y2="16" stroke="#00ffff" stroke-width="1" stroke-dasharray="2,2" />
            </svg>
            <div class="label-clickable" style="animation-delay: 0.8s;" @click="onDeviceLabelClick('water')">水肥控制机</div>
          </div>
          <div class="absolute bottom-[30%] left-[58%]">
            <svg class="absolute left-1/2 -translate-x-1/2 -top-6 w-8 h-12 pointer-events-none" viewBox="0 0 32 48">
              <line x1="16" y1="48" x2="16" y2="8" stroke="#00ffff" stroke-width="1" stroke-dasharray="2,2" />
            </svg>
            <div class="label-clickable" style="animation-delay: 1s;" @click="onDeviceLabelClick('sensor')">环境传感器</div>
          </div>
        </div>
      </div>

      <!-- ========== RIGHT COLUMN ========== -->
      <div class="flex flex-col gap-4 overflow-y-auto custom-scrollbar pr-1 h-full">
        <PanelBox title="视听融合病虫害预警" subtitle="14:35:42">
          <div class="bg-red-500/20 border border-red-500 text-red-500 text-center py-1.5 rounded text-sm font-bold flex items-center justify-center gap-2 mb-3 shadow-[0_0_10px_rgba(255,0,0,0.3)]">
            <AlertTriangle :size="18" /> 检测到异常声学信号！
          </div>
          <div class="flex gap-3" style="height: 160px;">
            <div class="flex-1 relative"><Spectrogram /></div>
            <div class="w-[100px] flex flex-col gap-2 shrink-0">
              <div class="text-xs text-gray-400 mb-1">识别结果</div>
              <div class="bg-red-500/10 border border-red-500/30 p-2 rounded relative overflow-hidden">
                <div class="absolute left-0 top-0 bottom-0 w-1 bg-red-500"></div>
                <div class="text-white text-sm font-bold">钻心虫</div>
                <div class="text-red-400 text-[10px]">高置信度</div>
              </div>
              <div class="bg-red-500/10 border border-red-500/30 p-2 rounded relative overflow-hidden opacity-70">
                <div class="absolute left-0 top-0 bottom-0 w-1 bg-red-500"></div>
                <div class="text-white text-sm font-bold">根结线虫</div>
                <div class="text-red-400 text-[10px]">高置信度</div>
              </div>
              <div class="bg-green-500/10 border border-green-500/30 p-2 rounded relative overflow-hidden opacity-50">
                <div class="absolute left-0 top-0 bottom-0 w-1 bg-green-500"></div>
                <div class="text-white text-sm font-bold">蚜虫</div>
                <div class="text-green-400 text-[10px]">低风险</div>
              </div>
            </div>
          </div>
        </PanelBox>
        <PanelBox title="AI 决策与控制指令流" subtitle="14:35:42" class="flex-1">
          <div class="flex gap-1 mb-3 border-b border-[var(--color-border)]">
            <button v-for="t in rightTabs" :key="t.key"
                    @click="rightTab = t.key"
                    class="px-3 py-1.5 text-xs font-medium transition-all duration-200"
                    :class="rightTab === t.key
                      ? 'text-[var(--color-cyan-glow)] border-b-2 border-[var(--color-cyan-glow)]'
                      : 'text-gray-500 hover:text-gray-300'">
              {{ t.label }}
            </button>
          </div>
          <div class="flex-1 flex flex-col" style="min-height: 180px;">
            <DecisionTimeline v-if="rightTab === 'decision'" :logs="decisionLog" @select="onLogSelect" />
            <AlertPanel v-else :alerts="alerts" @dismiss="dismissAlert" @execute="executeAction" />
          </div>
        </PanelBox>
      </div>
    </div>

    <!-- Bottom Stats Bar -->
    <div class="grid grid-cols-7 gap-3 mt-3 shrink-0">
      <div v-for="(card, idx) in statCards" :key="idx"
           class="border border-[var(--color-border)] rounded-lg p-2.5 flex flex-col items-center justify-center relative overflow-hidden group hover:border-[var(--color-border-strong)] transition-colors text-center bg-transparent">
        <div class="absolute inset-0 bg-gradient-to-r from-[var(--color-cyan-dim)] to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
        <div class="flex flex-col items-center gap-2 relative z-10">
          <div class="p-1.5 rounded-lg" :class="card.isWarning ? 'bg-red-500/20 text-red-400' : 'bg-[var(--color-cyan-dim)] text-[var(--color-cyan-glow)]'">
            <component :is="card.icon" :size="16" />
          </div>
          <div class="flex flex-col items-center">
            <div class="text-xs text-gray-400 mb-0.5">{{ card.label }}</div>
            <div class="flex items-baseline gap-1 justify-center">
              <span class="text-xl font-bold num-font" :class="card.isWarning ? 'text-red-400' : 'text-white'">{{ card.value }}</span>
              <span class="text-xs text-gray-400">{{ card.unit }}</span>
              <span v-if="card.trend" class="text-green-500 text-xs ml-1">↑</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Time Playback Slider -->
    <div class="flex items-center gap-3 mt-2 px-3 py-2 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-panel)]/30 shrink-0">
      <button @click="isPlaying = !isPlaying"
              class="p-1 rounded transition-colors"
              :class="isPlaying ? 'text-[var(--color-cyan-glow)]' : 'text-gray-500 hover:text-gray-300'">
        <svg v-if="isPlaying" class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/></svg>
        <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
      </button>
      <div class="flex-1 relative">
        <input type="range" min="0" max="23" v-model.number="playbackHour"
               class="w-full h-1 appearance-none rounded-full outline-none cursor-pointer"
               style="background: linear-gradient(90deg, var(--color-cyan-glow) 0%, rgba(0,255,204,0.1) 100%);" />
        <div class="flex justify-between text-[9px] text-gray-600 mt-0.5 px-0.5">
          <span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span>
        </div>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <span class="text-[10px] text-gray-500">时间穿梭</span>
        <span class="text-xs font-bold num-font text-[var(--color-cyan-glow)]">{{ displayTime }}</span>
      </div>
    </div>
  </div>

  <!-- Device Detail Modal -->
  <Teleport to="body">
    <transition name="fade">
      <div v-if="selectedDevice" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm"
           @click.self="selectedDevice = null">
        <div class="w-[440px] rounded-xl border border-[var(--color-border-strong)] bg-[#0a1a28] backdrop-blur-xl p-0 shadow-2xl overflow-hidden">
          <!-- Header with device icon -->
          <div class="relative px-6 pt-6 pb-4 bg-gradient-to-br from-[var(--color-cyan-dim)] to-transparent border-b border-[var(--color-border)]">
            <div class="flex justify-between items-start">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-[var(--color-cyan-glow)]/20 to-[var(--color-jade)]/20 border border-[var(--color-border)] flex items-center justify-center">
                  <component :is="deviceIconComp(selectedDevice.category)" :size="24" class="text-[var(--color-cyan-glow)]" />
                </div>
                <div>
                  <h3 class="text-lg font-bold text-white">{{ selectedDevice.name }}</h3>
                  <div class="flex items-center gap-2 mt-1">
                    <span class="text-[11px] text-gray-500">ID: {{ selectedDevice.id.toUpperCase() }}</span>
                    <span class="text-[10px] text-gray-600">|</span>
                    <span class="text-[11px] text-gray-500">{{ selectedDevice.categoryLabel }}</span>
                  </div>
                </div>
              </div>
              <button @click="selectedDevice = null" class="w-7 h-7 rounded-lg flex items-center justify-center text-gray-500 hover:text-white hover:bg-white/5 transition-all">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
          </div>

          <div class="px-6 py-4 space-y-4">
            <!-- Status & Value row -->
            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 rounded-lg border border-[var(--color-border)] bg-black/30">
                <div class="text-[10px] text-gray-500 uppercase tracking-wider mb-2">运行状态</div>
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full" :class="isDeviceOn ? 'bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.6)] animate-pulse' : 'bg-gray-600'"></span>
                  <span class="text-sm font-bold" :class="isDeviceOn ? 'text-green-400' : 'text-gray-400'">
                    {{ isDeviceOn ? '运行中' : '已关闭' }}
                  </span>
                </div>
              </div>
              <div class="p-3 rounded-lg border border-[var(--color-border)] bg-black/30">
                <div class="text-[10px] text-gray-500 uppercase tracking-wider mb-2">当前输出</div>
                <div class="text-sm font-bold text-white num-font">{{ selectedDevice.value }}<span class="text-gray-500 text-xs ml-0.5">%</span></div>
              </div>
            </div>

            <!-- Description -->
            <div class="p-3 rounded-lg border border-[var(--color-border)] bg-black/20">
              <div class="text-[10px] text-gray-500 uppercase tracking-wider mb-1.5">设备说明</div>
              <p class="text-xs text-gray-300 leading-relaxed">{{ deviceDescription }}</p>
            </div>

            <!-- Value bar -->
            <div>
              <div class="flex justify-between text-[10px] text-gray-500 mb-1">
                <span>输出功率</span>
                <span class="num-font">{{ selectedDevice.value }}%</span>
              </div>
              <div class="h-2 rounded-full bg-black/40 border border-[var(--color-border)] overflow-hidden">
                <div class="h-full rounded-full transition-all duration-500"
                     :style="{ width: selectedDevice.value + '%', background: valueBarGradient }"></div>
              </div>
            </div>

            <!-- Info grid -->
            <div class="grid grid-cols-3 gap-2">
              <div class="p-2 rounded border border-[var(--color-border)] bg-black/20 text-center">
                <div class="text-[10px] text-gray-500 mb-0.5">电压</div>
                <div class="text-xs font-bold text-white num-font">220V</div>
              </div>
              <div class="p-2 rounded border border-[var(--color-border)] bg-black/20 text-center">
                <div class="text-[10px] text-gray-500 mb-0.5">功率</div>
                <div class="text-xs font-bold text-white num-font">{{ selectedDevice.value * 2.5 }}W</div>
              </div>
              <div class="p-2 rounded border border-[var(--color-border)] bg-black/20 text-center">
                <div class="text-[10px] text-gray-500 mb-0.5">更新时间</div>
                <div class="text-xs font-bold text-white num-font">14:35</div>
              </div>
            </div>
          </div>

          <!-- Control button -->
          <div class="px-6 pb-6 pt-2">
            <button @click="onToggleDevice"
                    class="w-full py-2.5 rounded-lg font-bold text-sm transition-all duration-300 flex items-center justify-center gap-2"
                    :class="isDeviceOn
                      ? 'bg-red-500/10 text-red-400 border border-red-500/40 hover:bg-red-500/20 hover:shadow-[0_0_15px_rgba(255,50,50,0.15)]'
                      : 'bg-[var(--color-cyan-dim)] text-[var(--color-cyan-glow)] border border-[var(--color-border-strong)] hover:shadow-[0_0_20px_rgba(0,255,204,0.2)]'">
              <svg v-if="isDeviceOn" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              {{ isDeviceOn ? '关闭设备' : '开启设备' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Line } from 'vue-chartjs'
import { AlertTriangle, Home, Box, Wifi, Activity, Droplets, CloudSun, Thermometer, Layers, Wind, Sun, Cloud } from 'lucide-vue-next'
import PanelBox from '@/components/PanelBox.vue'
import RadarChart from './RadarChart.vue'
import NDVICanvas from './NDVICanvas.vue'
import Spectrogram from './Spectrogram.vue'
import DecisionTimeline from './DecisionTimeline.vue'
import AlertPanel from './AlertPanel.vue'
import { decisionLog, useSensorData } from '@/composables/useSensorData'

const { devices, toggleDevice, alerts, dismissAlert, executeAction } = useSensorData()
const selectedDevice = ref(null)
const rightTab = ref('decision')
const isPlaying = ref(false)
const playbackHour = ref(-1)

const displayTime = computed(() => {
  if (playbackHour.value < 0) return new Date().toLocaleTimeString('zh-CN', { hour12: false })
  return `${String(playbackHour.value).padStart(2, '0')}:00:00`
})

const rightTabs = computed(() => [
  { key: 'decision', label: '决策流' },
  { key: 'alerts', label: `告警 (${alerts.length})` },
])

const onLogSelect = (log) => {}

// ============================================
// Device label click → modal
// ============================================
const onDeviceLabelClick = (id) => {
  let device
  if (['drone', 'robot', 'sensor'].includes(id)) {
    device = virtualDevices[id]
  } else {
    device = devices.find(d => d.id === id)
  }
  if (device) {
    selectedDevice.value = {
      ...device,
      categoryLabel: categoryLabel(device.category)
    }
  }
}

const virtualDevices = {
  drone:  { id: 'drone',  name: '多光谱无人机', status: 'on', value: 78, category: 'drone' },
  robot:  { id: 'robot',  name: '巡检机器人',   status: 'on', value: 92, category: 'robot' },
  sensor: { id: 'sensor', name: '环境传感器',   status: 'on', value: 55, category: 'sensor' },
}

const isDeviceOn = computed(() => {
  return selectedDevice.value?.status === 'on' || selectedDevice.value?.status === 'running'
})

const categoryLabel = (cat) => {
  const map = { ventilation: '通风', lighting: '照明', irrigation: '灌溉', shading: '遮阳', heating: '加热', co2: 'CO₂', drone: '巡检', robot: '巡检', sensor: '监测' }
  return map[cat] || '其他'
}

const deviceIconComp = (cat) => {
  const map = { ventilation: Wind, lighting: Sun, irrigation: Droplets, shading: Cloud, heating: Thermometer, co2: Wind, drone: Cloud, robot: Activity, sensor: Thermometer }
  return map[cat] || Activity
}

const deviceDescription = computed(() => {
  const desc = {
    fan: '变频调速通风系统，根据温湿度自动调节风量，维持棚内空气流通环境。',
    light: '全光谱LED植物补光灯，模拟自然光照，支持多段调光模式。',
    water: '智能水肥一体化灌溉系统，精准控制施肥量与灌溉量。',
    shade: '电动遮阳帘系统，自动调节光照强度，保护药材免受强光灼伤。',
    heater: '恒温加热系统，确保低温环境下棚内温度维持在适宜范围。',
    co2: 'CO₂浓度智能调控系统，根据光合作用需求自动补充二氧化碳。',
    drone: '搭载多光谱相机，可执行自主航线巡检，实时回传作物生长数据。',
    robot: '地面巡检机器人，集成声学传感器与视觉摄像头，全天候监测病虫害。',
    sensor: '多参数环境传感器节点，实时采集温湿度、光照、CO₂等数据。',
  }
  return desc[selectedDevice.value?.id] || '智能农业设备'
})

const valueBarGradient = computed(() => {
  const v = selectedDevice.value?.value || 0
  if (v > 70) return 'linear-gradient(90deg, #22c55e, #4ecdc4)'
  if (v > 30) return 'linear-gradient(90deg, #22c55e, #eab308)'
  return 'linear-gradient(90deg, #ef4444, #eab308)'
})

const onToggleDevice = () => {
  if (!selectedDevice.value) return
  const devId = selectedDevice.value.id
  if (['drone', 'robot', 'sensor'].includes(devId)) {
    const vd = virtualDevices[devId]
    vd.status = vd.status === 'on' ? 'off' : 'on'
    vd.value = vd.status === 'on' ? (devId === 'drone' ? 78 : devId === 'robot' ? 92 : 55) : 0
    selectedDevice.value = { ...vd, categoryLabel: categoryLabel(vd.category) }
    return
  }
  toggleDevice(devId)
  const updated = devices.find(d => d.id === devId)
  if (updated) {
    selectedDevice.value = { ...updated, categoryLabel: categoryLabel(updated.category) }
  }
}

// ============================================
// Static data
// ============================================
const envMonitors = [
  { icon: Thermometer, label: '空气温度', val: '26.4', unit: '°C' },
  { icon: Droplets, label: '空气湿度', val: '68.2', unit: '%' },
  { icon: CloudSun, label: 'CO₂浓度', val: '613', unit: 'ppm' },
  { icon: Layers, label: '土壤湿度', val: '32.6', unit: '%' },
]

const statCards = [
  { icon: Home, label: '大棚总数', value: '12', unit: '个' },
  { icon: Box, label: '种植面积', value: '85.6', unit: '亩' },
  { icon: Wifi, label: '设备在线率', value: '98.7', unit: '%' },
  { icon: AlertTriangle, label: '今日告警数', value: '3', unit: '次', isWarning: true },
  { icon: Activity, label: '今日干预次数', value: '18', unit: '次' },
  { icon: Activity, label: '累计增产预估', value: '+12.6', unit: '%', trend: true },
  { icon: Droplets, label: '节水节肥率', value: '23.4', unit: '%', trend: true },
]

const areaChartData = [
  { time: '00:00', value: 3 }, { time: '04:00', value: 4 },
  { time: '08:00', value: 6 }, { time: '11:30', value: 8.76 },
  { time: '12:00', value: 9 }, { time: '16:00', value: 7 },
  { time: '20:00', value: 4 }, { time: '24:00', value: 3 },
]

const lineChartData = computed(() => ({
  labels: areaChartData.map(d => d.time),
  datasets: [{
    label: '蒸腾速率', data: areaChartData.map(d => d.value),
    fill: true, backgroundColor: 'rgba(0, 168, 255, 0.3)',
    borderColor: '#00ffff', borderWidth: 2, tension: 0.4,
    pointBackgroundColor: '#00ffff', pointRadius: 3,
  }]
}))

const lineChartOptions = {
  responsive: true, maintainAspectRatio: false,
  scales: {
    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b', font: { size: 10 } }, border: { display: false } },
    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b', font: { size: 10 } }, border: { display: false } },
  },
  plugins: {
    legend: { display: false },
    tooltip: { backgroundColor: 'rgba(2, 17, 36, 0.9)', borderColor: '#00ffff', borderWidth: 1 },
  }
}
</script>

<style scoped>
.label-clickable {
  background: rgba(0,255,255,0.1);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(0,255,255,0.5);
  padding: 6px 12px;
  border-radius: 6px;
  color: #00ffff;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  position: absolute;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: label-pulse 2s ease-in-out infinite;
}
.label-clickable:hover {
  background: rgba(0,255,255,0.25);
  border-color: #00ffff;
  box-shadow: 0 0 15px rgba(0,255,204,0.3);
  transform: scale(1.05);
}
@keyframes label-pulse {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}
</style>
