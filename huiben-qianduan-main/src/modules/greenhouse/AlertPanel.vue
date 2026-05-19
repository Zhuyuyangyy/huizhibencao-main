<template>
  <div class="flex flex-col gap-2">
    <div v-for="alert in alerts" :key="alert.id"
         class="group rounded-lg border p-3 cursor-pointer transition-all duration-300"
         :class="borderClass(alert.severity)"
         @click="selected = selected === alert.id ? null : alert.id">

      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="p-1 rounded-full" :class="iconBgClass(alert.severity)">
            <AlertTriangle :size="14" :class="iconColorClass(alert.severity)" />
          </div>
          <div>
            <span class="text-sm font-medium text-white">{{ alert.message }}</span>
            <div class="flex items-center gap-2 mt-0.5">
              <span class="text-[10px] text-gray-500">{{ alert.time }}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded-full"
                    :class="severityBadgeClass(alert.severity)">
                {{ severityText(alert.severity) }}
              </span>
            </div>
          </div>
        </div>
        <svg class="w-4 h-4 text-gray-500 transition-transform duration-300"
             :class="{ 'rotate-180': selected === alert.id }"
             fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>

      <!-- Expanded: Recommendation + Execute -->
      <transition name="expand">
        <div v-if="selected === alert.id" class="mt-3 pt-3 border-t border-[var(--color-border)]">
          <p class="text-xs text-gray-400 mb-3 leading-relaxed">{{ alert.desc }}</p>
          <div class="flex gap-2">
            <button @click.stop="dismiss(alert.id)"
                    class="flex-1 py-1.5 rounded text-xs font-medium border border-[var(--color-border)] text-gray-400 hover:text-white hover:border-[var(--color-border-strong)] transition-all">
              忽略
            </button>
            <button @click.stop="execute(alert.id)"
                    class="flex-1 py-1.5 rounded text-xs font-bold transition-all"
                    :class="executeBtnClass(alert.severity)">
              一键执行
            </button>
          </div>
        </div>
      </transition>
    </div>

    <div v-if="alerts.length === 0" class="text-center py-6">
      <svg class="w-8 h-8 mx-auto text-green-500/50 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-xs text-green-500/70">暂无告警，系统运行正常</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { AlertTriangle } from 'lucide-vue-next'

const props = defineProps({
  alerts: { type: Array, default: () => [] }
})

const emit = defineEmits(['dismiss', 'execute'])
const selected = ref(null)

const dismiss = (id) => { emit('dismiss', id); if (selected.value === id) selected.value = null }
const execute = (id) => { emit('execute', id); selected.value = null }

const borderClass = (sev) => {
  if (sev === 'danger') return 'border-red-500/30 bg-red-500/5 hover:bg-red-500/10'
  if (sev === 'warning') return 'border-yellow-500/30 bg-yellow-500/5 hover:bg-yellow-500/10'
  return 'border-blue-500/20 bg-blue-500/5 hover:bg-blue-500/10'
}
const iconBgClass = (sev) => {
  if (sev === 'danger') return 'bg-red-500/20'
  if (sev === 'warning') return 'bg-yellow-500/20'
  return 'bg-blue-500/20'
}
const iconColorClass = (sev) => {
  if (sev === 'danger') return 'text-red-400'
  if (sev === 'warning') return 'text-yellow-400'
  return 'text-blue-400'
}
const severityBadgeClass = (sev) => {
  if (sev === 'danger') return 'bg-red-500/10 text-red-400'
  if (sev === 'warning') return 'bg-yellow-500/10 text-yellow-400'
  return 'bg-blue-500/10 text-blue-400'
}
const severityText = (sev) => {
  if (sev === 'danger') return '紧急'
  if (sev === 'warning') return '重要'
  return '一般'
}
const executeBtnClass = (sev) => {
  if (sev === 'danger') return 'bg-red-500/20 text-red-400 border border-red-500/50 hover:bg-red-500/30'
  if (sev === 'warning') return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/50 hover:bg-yellow-500/30'
  return 'bg-blue-500/20 text-blue-400 border border-blue-500/50 hover:bg-blue-500/30'
}
</script>

<style scoped>
.expand-enter-active { transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
.expand-leave-active { transition: all 0.15s ease; }
.expand-enter-from, .expand-leave-to { opacity: 0; max-height: 0; overflow: hidden; }
.expand-enter-to, .expand-leave-from { opacity: 1; max-height: 200px; overflow: hidden; }
</style>
