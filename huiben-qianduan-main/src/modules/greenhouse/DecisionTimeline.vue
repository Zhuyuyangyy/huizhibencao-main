<template>
  <div class="flex flex-col gap-3 overflow-y-auto pr-2 custom-scrollbar flex-1">
    <div v-for="(log, index) in logs" :key="index" class="flex gap-3 items-start relative pb-2 group cursor-pointer"
         @click="$emit('select', log)">
      <div v-if="index !== logs.length - 1" class="absolute left-[15px] top-8 bottom-[-10px] w-px bg-[var(--color-border)]"></div>
      <div class="relative z-10 p-1.5 rounded-full mt-1 border"
           :class="statusClass(log.status)">
        <component :is="iconComponent(log.icon)" :size="16" v-if="iconComponent(log.icon)" />
      </div>
      <div class="flex-1 bg-[#041a33]/50 p-2 rounded border border-[var(--color-border)] group-hover:bg-[#041a33] transition-colors">
        <div class="flex justify-between items-center mb-1">
          <div class="font-bold text-sm"
               :class="log.status === 'alert' ? 'text-[var(--color-alert-danger)]' : 'text-[var(--color-cyan-glow)]'">
            {{ log.title }}
          </div>
          <div class="text-[10px] text-gray-500">{{ log.time }}</div>
        </div>
        <div class="text-xs text-gray-400">{{ log.desc }}</div>
      </div>
      <div class="mt-2 text-[10px] whitespace-nowrap">
        <span :class="statusTextClass(log.status)">{{ statusText(log.status) }}</span>
      </div>
    </div>
    <div class="text-center mt-2 cursor-pointer text-[var(--color-cyan-glow)]/70 text-xs flex items-center justify-center gap-1 hover:text-[var(--color-cyan-glow)]">
      查看更多日志
      <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { h } from 'vue'
import { Droplets, Layers, Wind, AlertTriangle, Sun, Cloud, Activity } from 'lucide-vue-next'

defineProps({
  logs: { type: Array, required: true }
})

defineEmits(['select'])

const iconMap = {
  droplet: Droplets,
  layers: Layers,
  wind: Wind,
  alert: AlertTriangle,
  sun: Sun,
  cloud: Cloud,
  activity: Activity,
}

const iconComponent = (name) => iconMap[name] || Activity

const statusClass = (status) => {
  if (status === 'running') return 'bg-[var(--color-cyan-dim)] text-[var(--color-cyan-glow)] border-[var(--color-border-strong)]'
  if (status === 'alert') return 'bg-red-500/20 text-red-500 border-red-500/50'
  return 'bg-green-500/20 text-green-500 border-green-500/50'
}

const statusTextClass = (status) => {
  if (status === 'running') return 'text-[var(--color-cyan-glow)]'
  if (status === 'alert') return 'text-red-500'
  return 'text-green-500'
}

const statusText = (status) => {
  if (status === 'running') return '执行中'
  if (status === 'alert') return '告警'
  return '已完成'
}
</script>
