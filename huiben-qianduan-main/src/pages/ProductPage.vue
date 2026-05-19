<template>
  <div>
    <!-- ============================================ -->
    <!-- HERO BANNER                                 -->
    <!-- ============================================ -->
    <section class="relative h-[60vh] min-h-[420px] flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0">
        <img src="/product-hero.webp" alt=""
             class="w-full h-full object-cover"
             style="filter: brightness(0.35) saturate(1.1);" />
        <div class="absolute inset-0 bg-gradient-to-b from-[var(--color-bg-base)]/40 via-transparent to-[var(--color-bg-base)]"></div>
      </div>
      <div class="absolute inset-0 opacity-[0.04] pointer-events-none"
           style="background-image: url('/logo-watermark.png'); background-size: 180px 180px; background-repeat: repeat; background-position: center;">
      </div>
      <div class="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-[var(--color-gold)] rounded-full blur-[150px] opacity-[0.04] pointer-events-none"></div>

      <div class="relative z-10 text-center px-6 max-w-4xl">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[var(--color-border)] bg-[var(--color-bg-panel)]/50 backdrop-blur-sm mb-8 animate-fade-in" style="animation-delay: 0.2s;">
          <span class="text-xs text-[var(--color-gold)] tracking-wider">产品简介</span>
        </div>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white font-serif leading-tight mb-6 animate-fade-in" style="animation-delay: 0.4s;">
          AI赋能中草药<br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-gold)] to-[var(--color-jade-light)]">全产业链智慧化解决方案</span>
        </h1>
        <p class="text-base md:text-lg text-[var(--color-text-secondary)] font-light max-w-2xl mx-auto leading-relaxed animate-fade-in" style="animation-delay: 0.6s;">
          从种植到流通，从监测到决策，构建道地中药材数字化生态
        </p>
      </div>
      <div class="absolute bottom-6 left-1/2 -translate-x-1/2">
        <svg class="w-5 h-5 text-gray-500 animate-bounce-down" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7" />
        </svg>
      </div>
    </section>

    <!-- ============================================ -->
    <!-- PROJECT OVERVIEW                            -->
    <!-- ============================================ -->
    <section class="relative py-20 px-6">
      <div class="max-w-7xl mx-auto">
        <div ref="overviewRef" class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center opacity-0 translate-y-8"
             :class="{ 'is-visible': overviewVisible }">
          <!-- Left text -->
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-border)] bg-[var(--color-cyan-dim)] mb-5">
              <span class="text-xs text-[var(--color-cyan-glow)]">项目概述</span>
            </div>
            <h2 class="text-3xl font-bold text-white font-serif mb-5 leading-tight">
              让道地中药材<br>
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-cyan-glow)] to-[var(--color-jade-light)]">拥抱数字时代</span>
            </h2>
            <div class="w-12 h-0.5 bg-[var(--color-cyan-glow)] mb-5"></div>
            <p class="text-sm text-[var(--color-text-secondary)] leading-relaxed mb-4">
              慧植本草·方寸灵畦项目立足"华佗故里"安徽亳州，以道地中药材智慧种植为核心，融合物联网、AI、大数据等前沿技术，打造覆盖"种-管-护-收"全流程的智慧农业解决方案。
            </p>
            <p class="text-sm text-[var(--color-text-muted)] leading-relaxed">
              项目以科技赋能传统中药材种植，通过数字化手段提升药材品质与产量，同时结合文旅融合与品牌建设，推动乡村产业振兴。
            </p>
          </div>

          <!-- Right stats -->
          <div class="grid grid-cols-2 gap-4">
            <div v-for="(stat, idx) in overviewStats" :key="idx"
                 class="p-5 rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-panel)]/50 backdrop-blur-sm text-center">
              <div class="text-3xl font-bold num-font text-transparent bg-clip-text bg-gradient-to-br from-[var(--color-cyan-glow)] to-[var(--color-jade-light)] mb-1">
                {{ stat.value }}
              </div>
              <div class="text-xs text-[var(--color-text-secondary)]">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================ -->
    <!-- "种管没收" TIMELINE                         -->
    <!-- ============================================ -->
    <section ref="timelineRef" class="relative py-20 px-6">
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[var(--color-border)] to-transparent"></div>
      <div class="max-w-5xl mx-auto">
        <div ref="timelineHeaderRef" class="text-center mb-14 opacity-0 translate-y-8" :class="{ 'is-visible': timelineVisible }">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-border)] bg-[var(--color-cyan-dim)] mb-5">
            <span class="text-xs text-[var(--color-cyan-glow)]">全流程追溯</span>
          </div>
          <h2 class="text-3xl font-bold text-white font-serif mb-3">种 · 管 · 护 · 收</h2>
          <p class="text-sm text-[var(--color-text-muted)]">点击各阶段查看详细流程</p>
        </div>
        <div class="opacity-0 translate-y-8" :class="{ 'is-visible': timelineVisible }" style="transition-delay: 200ms;">
          <TimelineFlow />
        </div>
      </div>
    </section>

    <!-- ============================================ -->
    <!-- FOUR FEATURES                               -->
    <!-- ============================================ -->
    <section ref="featuresRef" class="relative py-20 px-6">
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[var(--color-border)] to-transparent"></div>
      <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-[var(--color-jade)] rounded-full blur-[200px] opacity-[0.02] pointer-events-none"></div>

      <div class="max-w-7xl mx-auto relative z-10">
        <div ref="featuresHeaderRef" class="text-center mb-14 opacity-0 translate-y-8" :class="{ 'is-visible': featuresVisible }">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-border)] bg-[var(--color-cyan-dim)] mb-5">
            <span class="text-xs text-[var(--color-cyan-glow)]">核心特色</span>
          </div>
          <h2 class="text-3xl font-bold text-white font-serif mb-3">四大核心特色</h2>
          <p class="text-sm text-[var(--color-text-muted)]">以科技重塑传统中药材种植的每一个环节</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <div v-for="(feat, idx) in features" :key="idx"
               class="opacity-0 translate-y-8"
               :class="{ 'is-visible': featuresVisible }"
               :style="{ transitionDelay: `${idx * 120}ms` }">
            <FeatureCard v-bind="feat" />
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================ -->
    <!-- CULTURAL TOURISM                            -->
    <!-- ============================================ -->
    <section ref="tourismRef" class="relative py-20 px-6">
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[var(--color-border)] to-transparent"></div>
      <div class="max-w-7xl mx-auto">
        <div ref="tourismHeaderRef" class="text-center mb-14 opacity-0 translate-y-8" :class="{ 'is-visible': tourismVisible }">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-border)] bg-[var(--color-gold)]/10 mb-5">
            <span class="text-xs text-[var(--color-gold)]">文旅融合</span>
          </div>
          <h2 class="text-3xl font-bold text-white font-serif mb-3">本草文旅 · 身心共养</h2>
          <p class="text-sm text-[var(--color-text-muted)]">传承中医药文化，打造沉浸式健康体验</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div v-for="(item, idx) in tourismItems" :key="idx"
               ref="tourismCardRefs"
               class="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-panel)]/30 backdrop-blur-sm p-6 opacity-0 translate-y-8 hover:border-[var(--color-border-strong)] transition-all duration-500"
               :class="{ 'is-visible': tourismCardsVisible }"
               :style="{ transitionDelay: `${idx * 150}ms` }">
            <div class="text-3xl mb-4">{{ item.emoji }}</div>
            <h3 class="text-lg font-bold text-white mb-3">{{ item.title }}</h3>
            <p class="text-sm text-[var(--color-text-muted)] leading-relaxed">{{ item.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'
import FeatureCard from '@/modules/product/FeatureCard.vue'
import TimelineFlow from '@/modules/product/TimelineFlow.vue'

// ============================================
// Scroll animations
// ============================================
const overviewRef = ref(null)
const overviewVisible = ref(false)
useIntersectionObserver(overviewRef, ([{ isIntersecting }]) => {
  if (isIntersecting) overviewVisible.value = true
}, { threshold: 0.3 })

const timelineRef = ref(null)
const timelineHeaderRef = ref(null)
const timelineVisible = ref(false)
useIntersectionObserver(timelineHeaderRef, ([{ isIntersecting }]) => {
  if (isIntersecting) timelineVisible.value = true
}, { threshold: 0.3 })

const featuresRef = ref(null)
const featuresHeaderRef = ref(null)
const featuresVisible = ref(false)
useIntersectionObserver(featuresHeaderRef, ([{ isIntersecting }]) => {
  if (isIntersecting) featuresVisible.value = true
}, { threshold: 0.3 })

const tourismRef = ref(null)
const tourismHeaderRef = ref(null)
const tourismVisible = ref(false)
const tourismCardRefs = ref([])
const tourismCardsVisible = ref(false)

useIntersectionObserver(tourismHeaderRef, ([{ isIntersecting }]) => {
  if (isIntersecting) tourismVisible.value = true
}, { threshold: 0.3 })

watch(tourismVisible, (v) => { if (v) tourismCardsVisible.value = true })

// ============================================
// Data
// ============================================
const overviewStats = [
  { value: '128+', label: '道地药材品种' },
  { value: '256', label: '智慧种植面积(亩)' },
  { value: '1,580+', label: '智能设备接入' },
  { value: '12', label: '标准化大棚' },
]

const features = [
  {
    image: '/feature-full-process.webp', emoji: '🌿', title: '全流程化',
    description: '从育苗定植到采收加工，全程数字化追踪管理，实现中药材全生命周期智慧管控。每个环节皆有数据记录，确保药材品质可追溯。',
  },
  {
    image: '/feature-data-driven.webp', emoji: '📊', title: '数据驱动',
    description: '200+传感器实时采集环境数据，AI算法精准分析生长态势。以数据替代经验，让每一个种植决策都有据可依。',
  },
  {
    image: '/feature-precision-ai.webp', emoji: '🎯', title: '精准智能',
    description: '声学识别+多光谱视觉双模融合，AI模型精准识别病虫害。自动推荐最优防治方案，精准到每一株药材。',
  },
  {
    image: '/feature-green-eco.webp', emoji: '♻️', title: '绿色高效',
    description: '智能水肥一体化系统，节水节肥率超23%。生物防治替代化学农药，绿色可持续种植模式。',
  },
]

const tourismItems = [
  {
    emoji: '🏛️', title: '中医药文化体验',
    description: '依托"华佗故里"文化底蕴，打造中医药文化展示馆。游客可近距离观摩道地药材种植过程，了解千年中医药文化精髓。',
  },
  {
    emoji: '🌿', title: '本草养生工坊',
    description: '结合二十四节气推出时令养生体验。游客可亲手采摘、炮制药材，参与五禽戏晨练、药膳品鉴等特色活动。',
  },
  {
    emoji: '📱', title: '智慧农业研学',
    description: '面向学生与农业从业者开展智慧农业研学课程。展示物联网监测、AI决策、无人机巡检等前沿技术在农业中的应用。',
  },
]
</script>

<style scoped>
@keyframes bounce-down {
  0%, 100% { transform: translateY(0); opacity: 0.5; }
  50% { transform: translateY(6px); opacity: 1; }
}
.animate-bounce-down { animation: bounce-down 2s ease-in-out infinite; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) both; }

.is-visible { animation: revealUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes revealUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
.opacity-0 { opacity: 0; }
.translate-y-8 { transform: translateY(30px); }
</style>
