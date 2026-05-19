<template>
  <div class="relative w-full h-full rounded-xl overflow-hidden">
    <!-- Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-[#021124] via-[#031a30] to-[#010e1a]"></div>
    <div class="absolute inset-0 opacity-[0.03]"
         style="background-image: radial-gradient(circle at 25px 25px, #00ffcc 1px, transparent 1px); background-size: 50px 50px;">
    </div>

    <!-- Greenhouse SVG outline -->
    <svg class="absolute inset-0 w-full h-full" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid meet">
      <rect x="40" y="30" width="320" height="240" rx="8"
            fill="none" stroke="rgba(0,255,204,0.15)" stroke-width="1.5" stroke-dasharray="4,4" />
      <line x1="173" y1="30" x2="173" y2="270" stroke="rgba(0,255,204,0.08)" stroke-width="1" />
      <line x1="227" y1="30" x2="227" y2="270" stroke="rgba(0,255,204,0.08)" stroke-width="1" />
      <g v-for="row in 3" :key="'row'+row">
        <circle v-for="plant in 8" :key="'p'+row+plant"
                :cx="60 + plant * 35" :cy="45 + row * 80"
                r="3" fill="rgba(0,255,204,0.12)" />
      </g>
    </svg>

    <!-- Device labels -->
    <div v-for="device in devicesWithPos" :key="device.id"
         class="absolute cursor-pointer group z-10"
         :style="{ top: device.pos.top, left: device.pos.left }"
         @click="$emit('deviceClick', device)">
      <svg v-if="device.lineStyle"
           class="absolute pointer-events-none"
           :style="{ ...device.lineStyle, width: '64px', height: '32px' }"
           viewBox="0 0 64 32">
        <line x1="0" y1="16" x2="60" y2="16" stroke="var(--color-cyan-glow)" stroke-width="1" stroke-dasharray="2,2" />
      </svg>
      <div class="bg-[rgba(0,255,255,0.08)] backdrop-blur-sm border border-[var(--color-border)] px-3 py-1.5 rounded text-[var(--color-cyan-glow)] text-xs font-medium whitespace-nowrap transition-all duration-300 group-hover:bg-[rgba(0,255,255,0.2)] group-hover:border-[var(--color-border-strong)] group-hover:shadow-[0_0_15px_rgba(0,255,204,0.2)]"
           :style="{ animationDelay: device.animDelay }">
        <div class="flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full"
                :class="device.status === 'on' || device.status === 'running'
                  ? 'bg-[var(--color-alert-success)] shadow-[0_0_6px_rgba(34,197,94,0.5)]'
                  : 'bg-gray-500'">
          </span>
          {{ device.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { devices } from '@/composables/useSensorData'

const deviceLayouts = [
  { id: 'fan',      pos: { top: '12%', left: '60%' }, lineStyle: { top: '-40px', left: '10px' }, animDelay: '0s' },
  { id: 'light',    pos: { top: '35%', left: '65%' }, lineStyle: { top: '-10px', left: '70px' }, animDelay: '0.4s' },
  { id: 'water',    pos: { top: '52%', left: '72%' }, lineStyle: { top: '-10px', left: '70px' }, animDelay: '0.8s' },
  { id: 'shade',    pos: { top: '28%', left: '25%' }, lineStyle: { top: '-40px', left: '-20px' }, animDelay: '1.0s' },
  { id: 'heater',   pos: { top: '68%', left: '18%' }, lineStyle: { top: '-10px', left: '-80px' }, animDelay: '1.2s' },
  { id: 'co2',      pos: { top: '15%', left: '15%' }, lineStyle: { top: '30px', left: '-10px' }, animDelay: '1.4s' },
]

const devicesWithPos = computed(() => {
  return devices.map(d => {
    const layout = deviceLayouts.find(p => p.id === d.id) || deviceLayouts[0]
    return { ...d, ...layout }
  })
})

defineEmits(['deviceClick'])
</script>
