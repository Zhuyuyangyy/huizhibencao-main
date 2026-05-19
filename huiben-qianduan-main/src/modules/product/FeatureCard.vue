<template>
  <div
    class="group relative rounded-xl overflow-hidden border border-[var(--color-border)] bg-[var(--color-bg-panel)]/30 backdrop-blur-sm cursor-pointer transition-all duration-500"
    :class="{ 'scale-[1.02] shadow-[0_0_40px_rgba(0,255,204,0.1)]': isHovered }"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <!-- Image -->
    <div class="relative h-52 overflow-hidden">
      <img :src="image" :alt="title"
           class="w-full h-full object-cover transition-all duration-700 ease-out"
           :class="isHovered ? 'scale-110' : 'scale-100'"
           style="filter: brightness(0.6) saturate(1.1);" />
      <div class="absolute inset-0 bg-gradient-to-t from-[var(--color-bg-base)] via-transparent to-transparent"></div>

      <!-- Hover glow overlay -->
      <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-br from-[var(--color-cyan-glow)]/10 to-transparent"></div>

      <!-- Emoji icon -->
      <div class="absolute top-4 left-4 w-10 h-10 rounded-lg flex items-center justify-center text-lg backdrop-blur-sm border border-white/10 bg-white/5
                  group-hover:scale-110 group-hover:border-[var(--color-cyan-glow)]/30 transition-all duration-300">
        {{ emoji }}
      </div>
    </div>

    <!-- Content -->
    <div class="p-6 relative">
      <h3 class="text-xl font-bold text-white mb-3 group-hover:text-[var(--color-cyan-glow)] transition-colors duration-300">{{ title }}</h3>
      <p class="text-sm text-[var(--color-text-muted)] leading-relaxed">{{ description }}</p>

      <!-- Corner accent -->
      <div class="absolute bottom-0 right-0 w-20 h-20 opacity-0 group-hover:opacity-100 transition-all duration-500">
        <svg viewBox="0 0 80 80" class="w-full h-full">
          <path d="M80 0v80H0" fill="none" stroke="var(--color-cyan-glow)" stroke-width="0.5" opacity="0.3"/>
        </svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  image: { type: String, required: true },
  title: { type: String, required: true },
  description: { type: String, default: '' },
  emoji: { type: String, default: '✨' },
})

const isHovered = ref(false)
</script>
