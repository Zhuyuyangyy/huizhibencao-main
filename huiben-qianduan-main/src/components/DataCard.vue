<template>
  <div
    class="relative rounded-lg p-4 cursor-pointer group transition-all duration-300 border"
    :class="[
      expanded ? 'border-[var(--color-border-strong)]' : 'border-[var(--color-border)] hover:border-[var(--color-border-strong)]',
      `bg-gradient-to-br from-[var(--color-bg-panel)] to-[var(--color-bg-base)]`,
    ]"
    :style="{
      boxShadow: expanded ? '0 0 20px rgba(0,255,204,0.08)' : 'none'
    }"
    @click="$emit('click')"
  >
    <!-- Icon + Label row -->
    <div class="flex items-center justify-between mb-2">
      <div class="flex items-center gap-2.5">
        <div
          class="w-9 h-9 rounded-lg flex items-center justify-center transition-all duration-300"
          :class="[
            variant === 'warning'
              ? 'bg-[var(--color-alert-warning)]/10 text-[var(--color-alert-warning)]'
              : variant === 'danger'
                ? 'bg-[var(--color-alert-danger)]/10 text-[var(--color-alert-danger)]'
                : 'bg-[var(--color-cyan-dim)] text-[var(--color-cyan-glow)]'
          ]"
        >
          <component :is="icon" v-if="icon" :size="18" />
          <span v-else class="text-lg font-bold">{{ emoji }}</span>
        </div>
        <span class="text-sm text-[var(--color-text-secondary)] font-medium">{{ label }}</span>
      </div>

      <!-- Expand indicator -->
      <div v-if="expandable" class="transition-transform duration-300" :class="{ 'rotate-180': expanded }">
        <svg class="w-4 h-4 text-[var(--color-text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>

    <!-- Value -->
    <div class="flex items-baseline gap-1.5">
      <span
        class="text-3xl font-bold num-font tracking-tight"
        :class="{
          'text-white': variant === 'default',
          'text-[var(--color-alert-warning)]': variant === 'warning',
          'text-[var(--color-alert-danger)]': variant === 'danger',
          'text-[var(--color-cyan-glow)]': variant === 'accent',
        }"
      >
        {{ displayValue }}
      </span>
      <span class="text-sm text-[var(--color-text-muted)]">{{ unit }}</span>
      <span v-if="trend" class="text-xs ml-1 flex items-center gap-0.5" :class="trend > 0 ? 'text-[var(--color-alert-success)]' : 'text-[var(--color-alert-danger)]'">
        <svg v-if="trend > 0" class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
        <svg v-else class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
        {{ Math.abs(trend) }}%
      </span>
    </div>

    <!-- Expanded Content -->
    <transition name="expand">
      <div v-if="expanded" class="mt-4 pt-4 border-t border-[var(--color-border)]">
        <slot name="expanded">
          <div class="text-sm text-[var(--color-text-secondary)]">暂无详细数据</div>
        </slot>
      </div>
    </transition>

    <!-- Hover glow -->
    <div class="absolute inset-0 rounded-lg bg-gradient-to-br from-[var(--color-cyan-glow)]/0 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], default: '' },
  unit: { type: String, default: '' },
  icon: { type: [Object, Function], default: null },
  emoji: { type: String, default: '' },
  variant: { type: String, default: 'default' },
  trend: { type: Number, default: 0 },
  expandable: { type: Boolean, default: false },
  expanded: { type: Boolean, default: false },
})

defineEmits(['click'])

const displayValue = computed(() => {
  if (props.value === '' || props.value === null) return '--'
  return props.value
})
</script>

<style scoped>
.expand-enter-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.expand-leave-active { transition: all 0.2s ease; }
.expand-enter-from, .expand-leave-to { opacity: 0; max-height: 0; }
.expand-enter-to, .expand-leave-from { max-height: 500px; }
</style>
