<template>
  <div class="relative">
    <!-- Timeline track -->
    <div class="relative flex items-center justify-between mb-12">
      <!-- Connecting line -->
      <div class="absolute left-[8%] right-[8%] top-1/2 -translate-y-1/2 h-px bg-gradient-to-r from-transparent via-[var(--color-border-strong)] to-transparent"></div>
      <div class="absolute left-[8%] right-[8%] top-1/2 -translate-y-1/2 h-[2px]"
           :style="{ background: `linear-gradient(90deg, var(--color-cyan-glow) ${progressPercent}%, rgba(0,255,204,0.1) ${progressPercent}%)` }">
      </div>

      <!-- Stage nodes -->
      <button v-for="(stage, idx) in stages" :key="stage.key"
              @click="activeStage = stage.key"
              class="relative z-10 flex flex-col items-center gap-2 group"
              :class="idx === 0 ? 'items-start' : idx === stages.length - 1 ? 'items-end' : 'items-center'">
        <!-- Node circle -->
        <div class="w-14 h-14 rounded-full flex items-center justify-center text-2xl transition-all duration-500 border-2"
             :class="activeStage === stage.key
               ? 'border-[var(--color-cyan-glow)] bg-[var(--color-cyan-dim)] shadow-[0_0_20px_rgba(0,255,204,0.3)] scale-110'
               : idx <= activeIndex
                 ? 'border-[var(--color-border-strong)] bg-[var(--color-bg-panel)]'
                 : 'border-[var(--color-border)] bg-black/30'">
          {{ stage.emoji }}
        </div>
        <!-- Label -->
        <span class="text-sm font-bold tracking-wider transition-colors duration-300"
              :class="activeStage === stage.key
                ? 'text-[var(--color-cyan-glow)]'
                : idx <= activeIndex ? 'text-white' : 'text-gray-500'">
          {{ stage.label }}
        </span>
      </button>
    </div>

    <!-- Active stage detail -->
    <transition name="slide-up" mode="out-in">
      <div v-if="activeDetail" :key="activeStage"
           class="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-panel)]/50 backdrop-blur-sm p-6 md:p-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-border)] bg-[var(--color-cyan-dim)] mb-4">
              <span class="text-xs text-[var(--color-cyan-glow)]">{{ activeDetail.subtitle }}</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">{{ activeDetail.title }}</h3>
            <p class="text-sm text-[var(--color-text-secondary)] leading-relaxed mb-4">{{ activeDetail.description }}</p>
            <div class="grid grid-cols-2 gap-3">
              <div v-for="(stat, si) in activeDetail.stats" :key="si"
                   class="p-3 rounded-lg border border-[var(--color-border)] bg-black/20">
                <div class="text-lg font-bold text-[var(--color-cyan-glow)] num-font">{{ stat.value }}</div>
                <div class="text-xs text-gray-400">{{ stat.label }}</div>
              </div>
            </div>
          </div>
          <div class="relative rounded-xl overflow-hidden h-48 md:h-64">
            <img :src="activeDetail.image" alt="" class="w-full h-full object-cover" style="filter: brightness(0.7);" />
            <div class="absolute inset-0 bg-gradient-to-tr from-[var(--color-bg-base)] via-transparent to-transparent"></div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const stages = [
  { key: 'seed', label: '种', emoji: '🌱' },
  { key: 'manage', label: '管', emoji: '📡' },
  { key: 'protect', label: '护', emoji: '🛡️' },
  { key: 'harvest', label: '收', emoji: '🌾' },
]

const stageDetails = {
  seed: {
    subtitle: '智慧育苗',
    title: '智能育种与种植规划',
    description: '基于土壤数据与气候模型，AI自动推荐适宜品种与种植方案。智能育苗室精准控制温光水气，确保种苗品质。',
    stats: [{ value: '98%', label: '出苗率' }, { value: '50+', label: '培育品种' }],
    image: '/feature-full-process.webp',
  },
  manage: {
    subtitle: '数字化管理',
    title: '全周期数字化精准管理',
    description: '物联网传感器实时监测环境参数，AI模型预测生长趋势。智能水肥一体化系统自动调节，实现精细化管控。',
    stats: [{ value: '23.4%', label: '节水节肥率' }, { value: '100%', label: '环境监控覆盖率' }],
    image: '/feature-data-driven.webp',
  },
  protect: {
    subtitle: '智能保护',
    title: 'AI病虫害预警与绿色防控',
    description: '声学识别+多光谱分析双模检测，病虫害预警准确率超92%。AI推荐最优防治方案，实现绿色生态种植。',
    stats: [{ value: '92%', label: '预警准确率' }, { value: '-45%', label: '农药使用量' }],
    image: '/feature-precision-ai.webp',
  },
  harvest: {
    subtitle: '高效采收',
    title: '精准采收与品质溯源',
    description: '基于生长模型预测最佳采收期。区块链溯源系统记录全周期数据，实现从田间到药房的全链条可追溯。',
    stats: [{ value: '+12.6%', label: '增产预估' }, { value: '100%', label: '可追溯覆盖率' }],
    image: '/feature-green-eco.webp',
  },
}

const activeStage = ref('seed')

const activeDetail = computed(() => stageDetails[activeStage.value])
const activeIndex = computed(() => stages.findIndex(s => s.key === activeStage.value))

const progressPercent = computed(() => {
  return ((activeIndex.value) / (stages.length - 1)) * 100
})
</script>

<style scoped>
.slide-up-enter-active { transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-up-leave-active { transition: all 0.25s ease; }
.slide-up-enter-from { opacity: 0; transform: translateY(20px); }
.slide-up-leave-to { opacity: 0; transform: translateY(-10px); }
</style>
