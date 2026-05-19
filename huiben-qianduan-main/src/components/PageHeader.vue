<template>
  <div class="mb-8">
    <div class="flex items-center gap-4 mb-3">
      <!-- Back button -->
      <button v-if="showBack" @click="$router.back()"
              class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm text-[var(--color-text-secondary)] hover:text-white hover:bg-white/5 transition-all duration-200">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        返回
      </button>

      <div class="flex-1">
        <h1 class="text-2xl font-bold text-white font-serif tracking-wider">{{ title }}</h1>
        <p v-if="subtitle" class="text-sm text-[var(--color-text-secondary)] mt-1">{{ subtitle }}</p>
      </div>

      <!-- Right slot -->
      <slot name="right" />
    </div>

    <!-- Decorative line -->
    <div class="relative h-px">
      <div class="absolute inset-0 bg-gradient-to-r from-[var(--color-border-strong)] via-[var(--color-cyan-glow)]/30 to-transparent"></div>
      <div class="absolute left-0 -top-[3px] w-1.5 h-[7px] bg-[var(--color-cyan-glow)] rounded-full shadow-[0_0_8px_rgba(0,255,204,0.5)]"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  showBack: { type: Boolean, default: false },
})
</script>
