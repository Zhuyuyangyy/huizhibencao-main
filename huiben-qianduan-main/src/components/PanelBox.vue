<template>
  <div
    class="relative rounded-[var(--panel-radius)] panel-border"
    :class="[
      `bg-[var(--color-bg-panel)] backdrop-blur-md`,
      `border border-[var(--color-border)]`,
      hoverable ? 'hover:border-[var(--color-border-strong)] transition-colors duration-300' : '',
      className
    ]"
    :style="panelStyle"
  >
    <!-- Four-corner decorations -->
    <div class="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-[var(--color-cyan-glow)] opacity-60"></div>
    <div class="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-[var(--color-cyan-glow)] opacity-60"></div>
    <div class="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-[var(--color-cyan-glow)] opacity-60"></div>
    <div class="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-[var(--color-cyan-glow)] opacity-60"></div>

    <!-- Title -->
    <div v-if="title" class="flex items-center gap-2 mb-4 px-4 pt-4">
      <span class="text-[var(--color-cyan-glow)] font-bold italic text-lg leading-none">//</span>
      <h3 class="text-base font-bold text-white tracking-wide">{{ title }}</h3>
      <div class="flex-1 h-px bg-gradient-to-r from-[var(--color-border)] to-transparent ml-2"></div>
      <span v-if="subtitle" class="text-xs text-[var(--color-text-muted)]">{{ subtitle }}</span>
    </div>

    <!-- Content -->
    <div :class="[title ? 'px-4 pb-4' : 'p-4']">
      <slot />
    </div>

    <!-- Corner glow accents -->
    <div class="absolute -top-px -left-px w-8 h-8 bg-gradient-to-br from-[var(--color-cyan-glow)]/10 to-transparent pointer-events-none rounded-tl"></div>
    <div class="absolute -bottom-px -right-px w-8 h-8 bg-gradient-to-tl from-[var(--color-cyan-glow)]/10 to-transparent pointer-events-none rounded-br"></div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
  hoverable: { type: Boolean, default: false },
  className: { type: String, default: '' },
  panelStyle: { type: Object, default: () => ({}) }
})
</script>

<style scoped>
.panel-border {
  box-shadow: inset 0 0 30px rgba(0, 255, 204, 0.02);
}
</style>
