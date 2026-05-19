<template>
  <div class="flex flex-col lg:flex-row items-center lg:items-start gap-8 lg:gap-12">
    <!-- Wheel -->
    <div class="relative shrink-0" style="width: 360px; height: 360px;">
      <!-- Outer glow -->
      <div class="absolute inset-0 rounded-full" style="background: radial-gradient(circle, rgba(0,255,204,0.04) 0%, transparent 70%);"></div>

      <svg viewBox="0 0 200 200" class="w-full h-full drop-shadow-[0_0_40px_rgba(0,255,204,0.05)]">
        <!-- Season arc segments -->
        <path v-for="(arc, idx) in seasonArcs" :key="'arc'+idx"
              :d="arc.path" fill="none" :stroke="arc.color" stroke-width="3"
              :opacity="arc.opacity" stroke-linecap="round"
              class="transition-all duration-700" />

        <!-- Concentric decorative rings -->
        <circle cx="100" cy="100" r="92" fill="none" stroke="rgba(0,255,204,0.06)" stroke-width="0.5" />
        <circle cx="100" cy="100" r="72" fill="none" stroke="rgba(0,255,204,0.03)" stroke-width="0.5" stroke-dasharray="3,5" />
        <circle cx="100" cy="100" r="52" fill="none" stroke="rgba(196,168,106,0.04)" stroke-width="0.5" stroke-dasharray="2,6" />

        <!-- Season labels -->
        <text v-for="(sl, si) in seasonLabels" :key="'sl'+si"
              :x="sl.x" :y="sl.y" text-anchor="middle"
              :fill="sl.color" font-size="4.5" font-weight="600"
              opacity="0.6" style="font-family: var(--font-display); letter-spacing: 0.2em;">
          {{ sl.label }}
        </text>

        <!-- Solar term nodes -->
        <g v-for="(term, idx) in solarTerms" :key="term.id"
           class="cursor-pointer" @click="selectTerm(term)">
          <!-- Pulse ring for selected -->
          <circle v-if="selectedTerm?.id === term.id"
                  :cx="nodePositions[idx].x" :cy="nodePositions[idx].y" r="12"
                  fill="none" stroke="#00ffcc" stroke-width="1" opacity="0.3"
                  style="animation: ring-pulse 2.5s ease-out infinite" />
          <!-- Node circle -->
          <circle :cx="nodePositions[idx].x" :cy="nodePositions[idx].y"
                  :r="selectedTerm?.id === term.id ? 7.5 : 5"
                  :fill="selectedTerm?.id === term.id ? '#00ffcc' : '#0d2a3a'"
                  :stroke="selectedTerm?.id === term.id ? '#00ffcc' : 'rgba(0,255,204,0.2)'"
                  :stroke-width="selectedTerm?.id === term.id ? 2.5 : 1.5"
                  class="transition-all duration-400"
                  :style="{ filter: selectedTerm?.id === term.id ? 'drop-shadow(0 0 8px #00ffcc)' : 'none' }" />
          <!-- Label -->
          <text :x="nodePositions[idx].x" :y="nodePositions[idx].y + 18"
                text-anchor="middle"
                :fill="selectedTerm?.id === term.id ? '#00ffcc' : '#5a7a8a'"
                font-size="4.5" font-weight="500"
                class="transition-all duration-300"
                style="pointer-events: none; font-family: var(--font-body);">
            {{ term.name }}
          </text>
        </g>
      </svg>

      <!-- Center display -->
      <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div class="w-24 h-24 rounded-full border border-[var(--color-border)] bg-[var(--color-bg-panel)]/60 backdrop-blur-md flex flex-col items-center justify-center shadow-xl transition-all duration-500">
          <div class="text-3xl mb-1">{{ selectedTerm?.icon || '🌿' }}</div>
          <div class="text-sm font-bold text-[var(--color-cyan-glow)] font-serif leading-none">{{ selectedTerm?.name || '节气' }}</div>
          <div class="text-[8px] text-gray-500 mt-0.5">{{ selectedTerm?.enName || '' }}</div>
        </div>
      </div>
    </div>

    <!-- Detail panel -->
    <transition name="detail-enter" mode="out-in">
      <div v-if="selectedTerm" :key="selectedTerm.id" class="flex-1 min-w-0 max-w-xl">
        <!-- Header with season badge -->
        <div class="flex items-center gap-3 mb-4">
          <div class="px-3 py-1 rounded-full text-xs font-medium border"
               :class="seasonBadgeClass">
            {{ seasonLabel }}
          </div>
          <span class="text-sm text-gray-400">{{ selectedTerm.date }}</span>
          <span class="text-xs text-gray-600 ml-auto">{{ selectedTerm.enName }}</span>
        </div>

        <!-- Description with decorative quote -->
        <div class="relative pl-4 mb-5 border-l border-[var(--color-gold)]/30">
          <div class="absolute -top-2 -left-1 text-lg text-[var(--color-gold)]/30 font-serif">"</div>
          <p class="text-sm text-gray-300 leading-relaxed pt-2">{{ selectedTerm.desc }}</p>
        </div>

        <!-- Health + Farming cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-5">
          <div class="p-4 rounded-xl border border-[var(--color-border)] bg-gradient-to-br from-[var(--color-gold)]/5 to-transparent
                      hover:from-[var(--color-gold)]/8 transition-all duration-300">
            <div class="flex items-center gap-2 mb-2">
              <span class="w-6 h-6 rounded-md bg-[var(--color-gold)]/10 border border-[var(--color-gold)]/20 flex items-center justify-center text-xs">💚</span>
              <span class="text-xs font-bold text-[var(--color-gold)] uppercase tracking-wider">养生建议</span>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">{{ selectedTerm.healthTip }}</p>
          </div>
          <div class="p-4 rounded-xl border border-[var(--color-border)] bg-gradient-to-br from-[var(--color-cyan-glow)]/5 to-transparent
                      hover:from-[var(--color-cyan-glow)]/8 transition-all duration-300">
            <div class="flex items-center gap-2 mb-2">
              <span class="w-6 h-6 rounded-md bg-cyan-400/10 border border-cyan-400/20 flex items-center justify-center text-xs">🌾</span>
              <span class="text-xs font-bold text-[var(--color-cyan-glow)] uppercase tracking-wider">农事指南</span>
            </div>
            <p class="text-xs text-gray-300 leading-relaxed">{{ selectedTerm.farmingTip }}</p>
          </div>
        </div>

        <!-- Recommended herbs -->
        <div>
          <div class="flex items-center gap-2 mb-2">
            <span class="text-[10px] text-gray-500 uppercase tracking-wider">推荐药材</span>
            <span class="flex-1 h-px bg-gradient-to-r from-[var(--color-border)] to-transparent"></span>
          </div>
          <div class="flex items-center gap-2 flex-wrap">
            <span v-for="h in selectedTerm.herbs" :key="h"
                  class="px-3 py-1 rounded-full text-xs border border-[var(--color-border-strong)] text-[var(--color-cyan-glow)] bg-[var(--color-cyan-dim)] hover:bg-[var(--color-cyan-dim)]/70 transition-colors cursor-default">
              {{ h }}
            </span>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { solarTerms } from '@/data/solarTerms'

const selectedTerm = ref(solarTerms[6]) // 立夏 as default (current month)

const selectTerm = (term) => { selectedTerm.value = term }

const nodePositions = computed(() => {
  return solarTerms.map((_, i) => {
    const angle = (i * 15 - 90) * Math.PI / 180
    return { x: 100 + 82 * Math.cos(angle), y: 100 + 82 * Math.sin(angle) }
  })
})

function polarToCartesian(cx, cy, r, a) {
  const rad = (a - 90) * Math.PI / 180
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) }
}
function describeArc(cx, cy, r, start, end) {
  const s = polarToCartesian(cx, cy, r, end)
  const e = polarToCartesian(cx, cy, r, start)
  const large = (end - start) > 180 ? 1 : 0
  return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 0 ${e.x} ${e.y}`
}

const seasonArcs = computed(() => {
  // Spring: 立春(315°= -45) → 谷雨(0°)
  // Summer: 立夏(15°) → 大暑(60°)
  // Autumn: 立秋(105°) → 霜降(150°)
  // Winter: 立冬(195°) → 大寒(240°)
  return [
    { path: describeArc(100, 100, 90, -45, 0), color: '#4ecdc4', opacity: 0.3 },
    { path: describeArc(100, 100, 90, 15, 60), color: '#eab308', opacity: 0.25 },
    { path: describeArc(100, 100, 90, 105, 150), color: '#f97316', opacity: 0.25 },
    { path: describeArc(100, 100, 90, 195, 240), color: '#3b82f6', opacity: 0.25 },
  ]
})

const seasonLabels = computed(() => {
  return [
    { x: 100, y: 15, label: '春', color: '#4ecdc4' },
    { x: 185, y: 100, label: '夏', color: '#eab308' },
    { x: 100, y: 190, label: '秋', color: '#f97316' },
    { x: 15, y: 100, label: '冬', color: '#3b82f6' },
  ]
})

const seasonBadgeClass = computed(() => {
  const map = {
    spring: 'border-cyan-400/30 text-cyan-400 bg-cyan-400/5',
    summer: 'border-yellow-400/30 text-yellow-400 bg-yellow-400/5',
    autumn: 'border-orange-400/30 text-orange-400 bg-orange-400/5',
    winter: 'border-blue-400/30 text-blue-400 bg-blue-400/5',
  }
  return map[selectedTerm.value?.season] || ''
})

const seasonLabel = computed(() => {
  const map = { spring: '春季', summer: '夏季', autumn: '秋季', winter: '冬季' }
  return map[selectedTerm.value?.season] || ''
})
</script>

<style scoped>
@keyframes ring-pulse {
  0% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.08; transform: scale(1.4); }
  100% { opacity: 0.3; transform: scale(1); }
}

.detail-enter-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.detail-leave-active {
  transition: all 0.2s ease;
}
.detail-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.detail-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
