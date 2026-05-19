<template>
  <div class="px-4 py-3 h-full flex flex-col relative overflow-hidden">
    <!-- Background image (original style) -->
    <div class="absolute inset-0 bg-[url('/hui-background1.jpg')] bg-cover bg-center brightness-110 pointer-events-none"></div>
    <div class="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[#00ffff] rounded-full blur-[150px] opacity-5 pointer-events-none"></div>

    <!-- Monitor mode tabs -->
    <div class="flex justify-center mb-3 shrink-0 relative z-10">
      <div class="bg-[#021124]/80 backdrop-blur-md border border-[var(--color-border)] rounded-xl p-1.5 flex gap-2">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="currentTab = tab.key"
          class="px-8 py-2.5 rounded-lg font-bold text-sm tracking-wide transition-all duration-300"
          :class="currentTab === tab.key
            ? 'bg-gradient-to-r from-[var(--color-cyan-glow)] to-[var(--color-jade-light)] text-[#021124] shadow-[0_0_20px_rgba(0,255,204,0.4)]'
            : 'text-[var(--color-cyan-glow)] hover:bg-[var(--color-cyan-dim)]'"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Monitor Content -->
    <div class="flex-1 flex flex-col min-h-0 relative z-10">
      <GreenhousePanel v-if="currentTab === 'greenhouse'" />
      <OpenFieldPanel v-else />
    </div>

    <!-- Export button -->
    <div class="absolute bottom-4 right-4 z-20">
      <button @click="doExport"
              :disabled="exporting"
              class="flex items-center gap-2 px-4 py-2 rounded-xl bg-[var(--color-jade)]/80 hover:bg-[var(--color-jade)] text-white text-sm font-medium backdrop-blur-md border border-[var(--color-border)] transition-all duration-300 disabled:opacity-50">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        {{ exporting ? '导出中...' : '导出Excel' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import GreenhousePanel from '@/modules/greenhouse/GreenhousePanel.vue'
import OpenFieldPanel from '@/modules/openfield/OpenFieldPanel.vue'
import { triggerExport } from '@/api'

const currentTab = ref('greenhouse')
const exporting = ref(false)
const tabs = [
  { key: 'greenhouse', label: '🌿 有棚区' },
  { key: 'openfield', label: '🌾 无棚区' },
]

const doExport = async () => {
  exporting.value = true
  try {
    // Download the Excel file
    const link = document.createElement('a')
    link.href = 'http://localhost:8000/api/export/excel'
    link.download = `慧植本草_数据_${new Date().toISOString().slice(0, 10)}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } finally {
    setTimeout(() => { exporting.value = false }, 1000)
  }
}
</script>
