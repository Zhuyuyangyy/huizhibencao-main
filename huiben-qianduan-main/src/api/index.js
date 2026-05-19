/**
 * API utility — connects frontend to backend server.
 * Uses Vite proxy (see vite.config.js) — no CORS issues.
 */

async function request(path, options = {}) {
  try {
    const res = await fetch(path, {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options,
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return await res.json()
  } catch (err) {
    console.error(`[API] ${path} failed:`, err.message)
    return null
  }
}

// ===== Sensor Data =====
export const fetchGreenhouse = () => request('/api/greenhouse')
export const fetchOpenfield = () => request('/api/openfield')
export const fetchDevices = () => request('/api/devices')
export const fetchAlerts = () => request('/api/alerts')
export const fetchRadar = () => request('/api/radar')
export const fetchSnapshot = () => request('/api/snapshot')

// ===== Soil Sensors =====
export const fetchSoilMoisture5 = () => request('/api/soil/moisture/5layer')
export const fetchSoilTempMoisture5 = () => request('/api/soil/temp-moisture/5layer')
export const fetchSoilMoisture3 = () => request('/api/soil/moisture/3layer')
export const fetchSoilTempMoisture3 = () => request('/api/soil/temp-moisture/3layer')
export const fetchSoilPH = () => request('/api/soil/ph')
export const fetchSoilEC = () => request('/api/soil/ec')
export const fetchNPK = () => request('/api/soil/npk')
export const fetchSoilAll = () => request('/api/soil/all')

// ===== Device Management =====
export const fetchDeviceInfo = () => request('/api/device/info')
export const syncDeviceTime = () => request('/api/device/time-sync', { method: 'POST' })
export const restartDevice = () => request('/api/device/restart', { method: 'POST' })

// ===== Alarm Management =====
export const fetchAlarmThresholds = () => request('/api/alarm/thresholds')
export const updateAlarmThreshold = (key, min, max) =>
  request(`/api/alarm/thresholds/${key}`, {
    method: 'PUT',
    body: JSON.stringify({ min, max }),
  })
export const checkAlarms = () => request('/api/alarm/check')

// ===== History =====
export const fetchHistory = (minutes = 60) => request(`/api/history?minutes=${minutes}`)
export const fetchStats = (minutes = 60) => request(`/api/stats?minutes=${minutes}`)

// ===== Excel Export =====
export const triggerExport = () => request('/api/export/excel')
export const fetchExportList = () => request('/api/export/list')

// ===== AI Chat =====
export const sendChatMessage = (question, withContext = true) =>
  request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ question, withContext }),
  })

// ===== Health =====
export const checkHealth = () => request('/api/health')
