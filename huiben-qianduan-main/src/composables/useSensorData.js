import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'
import { fetchGreenhouse, fetchOpenfield, fetchDevices, fetchAlerts } from '@/api'

// Current sensor values for greenhouse (fallback mock)
const greenhouseData = reactive({
  light: 15800,
  ph: 6.38,
  soilMoisture: 32.6,
  co2: 613,
  airHumidity: 68.2,
  airTemp: 26.4,
  potassium: 28.6,
  phosphorus: 192,
  ndvi: 0.72,
  transpiration: 4.5,
  ec: 1.2,
})

// Open field sensor values (fallback mock)
const openfieldData = reactive({
  airTemp: 28.6,
  airHumidity: 72.5,
  co2: 420,
  soilMoisture: 45.2,
  rainfall: 0,
  windSpeed: 2.3,
  windDir: '东南',
})

export const devices = reactive([
  { id: 'fan', name: '通风系统', status: 'on', value: 65, category: 'ventilation', icon: 'wind' },
  { id: 'light', name: 'LED补光灯', status: 'on', value: 60, category: 'lighting', icon: 'sun' },
  { id: 'water', name: '智能水肥机', status: 'running', value: 28, category: 'irrigation', icon: 'droplet' },
  { id: 'shade', name: '遮阳帘', status: 'off', value: 0, category: 'shading', icon: 'cloud' },
  { id: 'heater', name: '加热系统', status: 'off', value: 0, category: 'heating', icon: 'thermometer' },
  { id: 'co2', name: 'CO₂发生器', status: 'on', value: 45, category: 'co2', icon: 'wind' },
])

const defaultAlerts = [
  { id: 1, type: 'pest', message: '钻心虫声学信号增强', desc: '虫害声学识别模型检测到钻心虫活动信号增强，建议加强监测并考虑生物防治。', time: '14:34:42', severity: 'warning' },
  { id: 2, type: 'env', message: '棚内湿度偏高', desc: '当前空气湿度68.2%，超出适宜范围（50-65%），建议开启通风系统。', time: '14:28:15', severity: 'warning' },
  { id: 3, type: 'device', message: '水肥机管道压力异常', desc: '水肥机输出管道压力为0.42MPa，超出正常范围，建议检查管道是否堵塞。', time: '14:15:00', severity: 'danger' },
  { id: 4, type: 'env', message: '光照强度波动较大', desc: '过去30分钟光照强度在12000-18500lux间波动，建议检查补光灯运行状态。', time: '13:55:30', severity: 'info' },
]

export const alerts = ref([...defaultAlerts])

// === Live data polling ===
let _pollTimer = null
let _apiAvailable = false

async function _pollData() {
  try {
    const [ghRes, ofRes, devRes, alertRes] = await Promise.all([
      fetchGreenhouse(),
      fetchOpenfield(),
      fetchDevices(),
      fetchAlerts(),
    ])
    if (ghRes?.code === 0) {
      Object.assign(greenhouseData, ghRes.data)
      _apiAvailable = true
    }
    if (ofRes?.code === 0) Object.assign(openfieldData, ofRes.data)
    if (devRes?.code === 0) {
      const newDevices = devRes.data
      newDevices.forEach((nd) => {
        const existing = devices.find((d) => d.id === nd.id)
        if (existing) Object.assign(existing, nd)
      })
    }
    if (alertRes?.code === 0) alerts.value = alertRes.data
  } catch {
    _apiAvailable = false
  }
}

function startPolling(intervalMs = 3000) {
  if (_pollTimer) return
  _pollData() // immediate first fetch
  _pollTimer = setInterval(_pollData, intervalMs)
}

function stopPolling() {
  if (_pollTimer) {
    clearInterval(_pollTimer)
    _pollTimer = null
  }
}

const selectedDevice = ref(null)
const selectedAlert = ref(null)
const playbackTime = ref(null)

export function useSensorData() {
  const isPlayback = computed(() => playbackTime.value !== null)

  // Auto-start polling when first component mounts
  onMounted(() => startPolling())
  onUnmounted(() => stopPolling())

  const toggleDevice = (deviceId) => {
    const device = devices.find(d => d.id === deviceId)
    if (device) {
      device.status = device.status === 'on' ? 'off' : 'on'
      device.value = device.status === 'on' ? 50 : 0
    }
  }

  const dismissAlert = (alertId) => {
    alerts.value = alerts.value.filter(a => a.id !== alertId)
  }

  const executeAction = (alertId) => {
    // Simulate executing recommended action
    const alert = alerts.value.find(a => a.id === alertId)
    if (alert) {
      // Add to decision log
      decisionLog.unshift({
        time: new Date().toLocaleTimeString('zh-CN', { hour12: false }),
        title: `已执行: ${alert.message}`,
        desc: alert.desc,
        status: 'running',
      })
      dismissAlert(alertId)
    }
  }

  return {
    greenhouseData, openfieldData, devices, alerts,
    selectedDevice, selectedAlert,
    playbackTime, isPlayback,
    toggleDevice, dismissAlert, executeAction,
  }
}

// Decision log
export const decisionLog = reactive([
  { time: '14:35:30', title: '智能水肥机已开启', desc: '调整灌溉量至 28%，施用平衡肥', status: 'running', icon: 'droplet' },
  { time: '14:35:15', title: '无人机已派出巡检', desc: '执行多光谱巡检任务，区域：A3区块', status: 'running', icon: 'layers' },
  { time: '14:34:58', title: '通风系统已调整', desc: '湿度偏高，已将风机转速调至 65%', status: 'completed', icon: 'wind' },
  { time: '14:34:42', title: '检测到潜在虫害风险', desc: '钻心虫声学信号增强，建议加强监测', status: 'alert', icon: 'alert' },
  { time: '14:34:20', title: 'LED补光灯已开启', desc: '光照不足，已开启补光灯至 60%', status: 'completed', icon: 'sun' },
  { time: '14:33:55', title: '遮阳帘已关闭', desc: '夜间模式，遮阳帘自动关闭', status: 'completed', icon: 'cloud' },
])

// Radar chart data
export const radarData = [
  { subject: '光照(lux)', A: 15800, fullMark: 20000, unit: ' lux' },
  { subject: 'pH值', A: 6.38, fullMark: 14, unit: '' },
  { subject: '土壤湿度', A: 32.6, fullMark: 100, unit: '%' },
  { subject: 'CO₂浓度', A: 613, fullMark: 1000, unit: ' ppm' },
  { subject: '空气湿度', A: 68.2, fullMark: 100, unit: '%' },
  { subject: '空气温度', A: 26.4, fullMark: 50, unit: '°C' },
  { subject: '钾(K)', A: 28.6, fullMark: 100, unit: '%' },
  { subject: '磷(P)', A: 192, fullMark: 300, unit: ' mg/kg' },
]

// Open field stats
export const openFieldStats = [
  { icon: 'home', label: '田块总数', value: '24', unit: '个' },
  { icon: 'box', label: '种植面积', value: '156.8', unit: '亩' },
  { icon: 'wifi', label: '设备在线率', value: '95.2', unit: '%' },
  { icon: 'alert', label: '今日告警数', value: '5', unit: '次', isWarning: true },
  { icon: 'activity', label: '今日干预次数', value: '12', unit: '次' },
  { icon: 'trending', label: '累计增产预估', value: '+8.3', unit: '%', trend: true },
  { icon: 'droplet', label: '节水节肥率', value: '18.7', unit: '%', trend: true },
]
