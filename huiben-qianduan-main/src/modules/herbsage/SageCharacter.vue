<template>
  <div class="relative flex flex-col items-center">
    <!-- Jade aura portal -->
    <div class="relative w-44 h-48 md:w-52 md:h-56 flex items-center justify-center">
      <!-- Outer glow rings -->
      <div class="absolute inset-0 rounded-full" :style="auraRingStyle"></div>
      <div class="absolute inset-[15%] rounded-full border border-[var(--color-border)] opacity-30"
           style="animation: rotate-slow 20s linear infinite;"></div>
      <div class="absolute inset-[25%] rounded-full border border-dashed border-[var(--color-border)] opacity-20"
           style="animation: rotate-slow 30s linear infinite reverse;"></div>

      <!-- Character image with breathing animation -->
      <div class="relative z-10 breathe-animation w-full h-full">
        <img src="/laozu-full.png" alt="百草通灵"
             class="w-full h-full object-contain drop-shadow-[0_0_30px_rgba(0,255,204,0.2)]" />

        <!-- Shimmer overlay on hover -->
        <div class="absolute inset-0 bg-gradient-to-t from-transparent via-[var(--color-cyan-glow)]/0 to-transparent
                    opacity-0 hover:opacity-100 transition-opacity duration-700 pointer-events-none rounded-full"
             style="background: linear-gradient(180deg, transparent 0%, rgba(0,255,204,0.06) 50%, transparent 100%);">
        </div>
      </div>

      <!-- Floating leaves -->
      <div v-for="i in 6" :key="'leaf'+i"
           class="absolute pointer-events-none"
           :style="leafStyle(i)">
        <svg viewBox="0 0 20 20" class="w-full h-full" :style="{ opacity: 0.3 + (i * 0.05) }">
          <path d="M10 0 C10 0 18 5 18 10 C18 15 10 20 10 20 C10 20 2 15 2 10 C2 5 10 0 10 0Z"
                :fill="leafColors[i % leafColors.length]"
                opacity="0.4" />
        </svg>
      </div>
    </div>

    <!-- Name title with decorative lines -->
    <div class="mt-4 text-center relative">
      <div class="flex items-center gap-3 mb-1">
        <span class="h-px w-8 bg-gradient-to-l from-[var(--color-gold)]/40 to-transparent"></span>
        <h3 class="text-lg font-bold text-white font-serif tracking-[0.2em]">百 草 通 灵</h3>
        <span class="h-px w-8 bg-gradient-to-r from-[var(--color-gold)]/40 to-transparent"></span>
      </div>
      <p class="text-xs text-[var(--color-gold)] tracking-[0.3em]">灵 通 万 物</p>
    </div>

    <!-- Expression badge -->
    <div class="mt-3 px-4 py-1.5 rounded-full border backdrop-blur-sm transition-all duration-500"
         :style="expressionBadgeStyle">
      <div class="flex items-center gap-2">
        <span class="text-xs" :style="{ color: expressionColor }">{{ expressionText }}</span>
        <span class="text-xs">{{ expressionEmoji }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  expression: { type: String, default: 'happy' },
})

const leafColors = ['#4ecdc4', '#6b9f6b', '#2d8a6e', '#c4a86a', '#4ecdc4', '#6b9f6b']

const expressionText = computed(() => {
  const map = { happy: '慈眉善目', think: '沉吟思索', surprise: '颇为惊讶', worry: '眉头微蹙' }
  return map[props.expression] || '慈眉善目'
})

const expressionEmoji = computed(() => {
  const map = { happy: '😊', think: '🤔', surprise: '😮', worry: '😟' }
  return map[props.expression] || '😊'
})

const expressionColor = computed(() => {
  const map = { happy: '#4ecdc4', think: '#c4a86a', surprise: '#ffcc00', worry: '#ff6680' }
  return map[props.expression] || '#4ecdc4'
})

const expressionBadgeStyle = computed(() => {
  const map = {
    happy: { borderColor: 'rgba(78,205,196,0.3)', backgroundColor: 'rgba(78,205,196,0.08)' },
    think: { borderColor: 'rgba(196,168,106,0.3)', backgroundColor: 'rgba(196,168,106,0.08)' },
    surprise: { borderColor: 'rgba(255,204,0,0.3)', backgroundColor: 'rgba(255,204,0,0.08)' },
    worry: { borderColor: 'rgba(255,102,128,0.3)', backgroundColor: 'rgba(255,102,128,0.08)' },
  }
  return map[props.expression] || map.happy
})

const auraRingStyle = computed(() => {
  const map = {
    happy: 'rgba(78,205,196,0.06)',
    think: 'rgba(196,168,106,0.06)',
    surprise: 'rgba(255,204,0,0.06)',
    worry: 'rgba(255,102,128,0.04)',
  }
  const color = map[props.expression] || map.happy
  return {
    background: `radial-gradient(circle, ${color} 0%, transparent 60%)`,
    boxShadow: `inset 0 0 60px ${color}`,
  }
})

const leafStyle = (i) => {
  const configs = [
    { top: '5%', left: '-8%', size: '10px', delay: '0s', dur: '4s', driftX: '-15px', driftY: '-20px', rot: '0deg' },
    { top: '20%', right: '-10%', size: '8px', delay: '0.8s', dur: '5s', driftX: '12px', driftY: '-25px', rot: '45deg' },
    { top: '40%', left: '-6%', size: '12px', delay: '1.6s', dur: '3.5s', driftX: '-20px', driftY: '-15px', rot: '90deg' },
    { top: '60%', right: '-8%', size: '7px', delay: '2.4s', dur: '4.5s', driftX: '15px', driftY: '-30px', rot: '135deg' },
    { top: '75%', left: '-12%', size: '9px', delay: '3.2s', dur: '5.5s', driftX: '-10px', driftY: '-20px', rot: '180deg' },
    { top: '90%', right: '-6%', size: '11px', delay: '4s', dur: '4s', driftX: '18px', driftY: '-10px', rot: '225deg' },
  ]
  const c = configs[i - 1] || configs[0]
  return {
    top: c.top,
    [c.left ? 'left' : 'right']: c.left || c.right,
    width: c.size,
    height: c.size,
    animation: `leaf-drift ${c.dur} ease-in-out ${c.delay} infinite alternate`,
    '--drift-x': c.driftX,
    '--drift-y': c.driftY,
    '--rot': c.rot,
  }
}
</script>

<style scoped>
.breathe-animation {
  animation: breathe 4s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

@keyframes leaf-drift {
  0% { transform: translateY(0) translateX(0) rotate(0deg); opacity: 0; }
  20% { opacity: 0.6; }
  100% { transform: translateY(var(--drift-y)) translateX(var(--drift-x)) rotate(var(--rot)); opacity: 0.2; }
}
</style>
