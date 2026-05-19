<template>
  <div class="relative">
    <!-- ============================================ -->
    <!-- HERO SECTION                                -->
    <!-- ============================================ -->
    <section class="relative h-screen min-h-[700px] flex items-center justify-center overflow-hidden">
      <!-- Background -->
      <div class="absolute inset-0">
        <img src="/hero-bg.webp" alt=""
             class="w-full h-full object-cover"
             style="filter: brightness(0.4) saturate(1.2);" />
        <div class="absolute inset-0 bg-gradient-to-b from-[var(--color-bg-base)]/30 via-transparent to-[var(--color-bg-base)]"></div>
      </div>

      <!-- Logo watermark pattern -->
      <div class="absolute inset-0 opacity-[0.04] pointer-events-none"
           style="background-image: url('/logo-watermark.png'); background-size: 200px 200px; background-repeat: repeat; background-position: center;">
      </div>

      <!-- Ambient glow -->
      <div class="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[var(--color-cyan-glow)] rounded-full blur-[120px] opacity-[0.06] pointer-events-none"></div>

      <!-- Floating decorative elements -->
      <div class="absolute top-[20%] left-[-10%] animate-drift-slow pointer-events-none select-none">
        <img src="/drone-silhouette.webp" alt="" class="w-24 h-auto opacity-[0.15]" />
      </div>
      <div class="absolute bottom-[30%] right-[8%] animate-float-slow pointer-events-none select-none">
        <img src="/robot-scout.webp" alt="" class="w-20 h-auto opacity-[0.12]" />
      </div>

      <!-- Herbal particles -->
      <div class="absolute inset-0 pointer-events-none overflow-hidden">
        <div v-for="p in particles" :key="p.key"
             class="absolute rounded-full"
             :style="p.style">
        </div>
      </div>

      <!-- Center content -->
      <div class="relative z-10 text-center px-6 max-w-5xl mx-auto">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[var(--color-border)] bg-[var(--color-bg-panel)]/50 backdrop-blur-sm mb-8 animate-hero-item" style="animation-delay: 0.2s;">
          <div class="w-1.5 h-1.5 rounded-full bg-[var(--color-alert-success)] shadow-[0_0_8px_rgba(34,197,94,0.5)]"></div>
          <span class="text-xs text-[var(--color-text-secondary)] tracking-wider">AI 智慧农业 · 道地中药材</span>
        </div>

        <h1 class="text-5xl md:text-7xl lg:text-8xl font-bold text-white font-serif tracking-[0.05em] leading-tight mb-6 animate-hero-item" style="animation-delay: 0.4s;">
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-white via-[var(--color-cyan-glow)] to-[var(--color-jade-light)]">
            慧植本草
          </span>
          <span class="block mt-2 text-4xl md:text-5xl lg:text-6xl text-[var(--color-text-secondary)] font-light tracking-[0.15em]">
            方寸灵畦
          </span>
        </h1>

        <div class="flex items-center justify-center gap-4 mb-8 animate-hero-item" style="animation-delay: 0.6s;">
          <div class="w-16 h-px bg-gradient-to-r from-transparent to-[var(--color-border-strong)]"></div>
          <div class="w-2 h-2 rotate-45 border border-[var(--color-cyan-glow)]"></div>
          <div class="w-16 h-px bg-gradient-to-l from-transparent to-[var(--color-border-strong)]"></div>
        </div>

        <p class="text-lg md:text-xl text-[var(--color-text-secondary)] font-light tracking-wider max-w-2xl mx-auto leading-relaxed animate-hero-item" style="animation-delay: 0.8s;">
          AI赋能道地药材，数字振兴乡土本草
        </p>

        <div class="flex items-center justify-center gap-4 mt-10 animate-hero-item" style="animation-delay: 1s;">
          <router-link to="/monitor"
             class="px-8 py-3.5 rounded-xl bg-gradient-to-r from-[var(--color-cyan-glow)] to-[var(--color-jade-light)] text-[var(--color-bg-base)] font-bold text-sm tracking-wider hover:shadow-[0_0_30px_rgba(0,255,204,0.4)] transition-all duration-300 hover:scale-105">
            进入监测平台
          </router-link>
          <router-link to="/product"
             class="px-8 py-3.5 rounded-xl border border-[var(--color-border)] text-[var(--color-text-secondary)] font-medium text-sm tracking-wider hover:text-white hover:border-[var(--color-border-strong)] hover:bg-white/5 transition-all duration-300">
            了解更多
          </router-link>
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 scroll-indicator">
        <span class="text-xs text-[var(--color-text-muted)] tracking-widest">SCROLL</span>
        <svg class="w-4 h-4 text-[var(--color-cyan-glow)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7" />
        </svg>
      </div>
    </section>

    <!-- ============================================ -->
    <!-- PROJECT OVERVIEW                            -->
    <!-- ============================================ -->
    <section class="relative py-24 px-6">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <!-- Left: Description -->
          <div ref="overviewTextRef" class="opacity-0 translate-y-8" :class="{ 'is-visible': overviewVisible }">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-border)] bg-[var(--color-cyan-dim)] mb-6">
              <span class="text-xs text-[var(--color-cyan-glow)]">项目概览</span>
            </div>
            <h2 class="text-3xl md:text-4xl font-bold text-white font-serif mb-6 leading-tight">
              让每一株本草<br>
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-[var(--color-cyan-glow)] to-[var(--color-jade-light)]">都被智慧守护</span>
            </h2>
            <div class="w-12 h-0.5 bg-[var(--color-cyan-glow)] mb-6"></div>
            <p class="text-[var(--color-text-secondary)] leading-relaxed mb-4">
              慧植本草 · 方寸灵畦是一个以道地中药材智慧种植为核心的AI+农业项目。项目融合物联网传感、机器视觉、声学监测、多光谱遥感等前沿技术，为中药材种植提供全流程智能化解决方案。
            </p>
            <p class="text-[var(--color-text-muted)] leading-relaxed text-sm">
              从有棚区的精密环境调控到无棚区的无人机巡田，从百草通灵AI的节气养生智慧到二十四节气的农事指导，我们用科技的力量守护每一株本草的茁壮成长。
            </p>
          </div>

          <!-- Right: Stats -->
          <div ref="statsRef" class="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <div v-for="(stat, idx) in statItems" :key="idx"
                 class="text-center p-8 rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-panel)]/50 backdrop-blur-sm hover:border-[var(--color-border-strong)] transition-all duration-500 opacity-0 translate-y-8 stat-card-item"
                 :class="{ 'is-visible': statVisible }"
                 :style="{ transitionDelay: `${idx * 150}ms` }">
              <div class="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-br from-[var(--color-cyan-glow)] to-[var(--color-jade-light)] num-font mb-2">
                {{ stat.value }}<span class="text-2xl text-[var(--color-text-muted)]">{{ stat.unit }}</span>
              </div>
              <div class="text-sm text-[var(--color-text-secondary)]">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================ -->
    <!-- CORE FEATURES                               -->
    <!-- ============================================ -->
    <section class="relative py-24 px-6">
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[var(--color-jade)] rounded-full blur-[200px] opacity-[0.02] pointer-events-none"></div>

      <div class="max-w-7xl mx-auto relative z-10">
        <div ref="featuresHeaderRef" class="text-center mb-16 opacity-0 translate-y-8" :class="{ 'is-visible': featuresHeaderVisible }">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-border)] bg-[var(--color-cyan-dim)] mb-6">
            <span class="text-xs text-[var(--color-cyan-glow)]">核心特色</span>
          </div>
          <h2 class="text-3xl md:text-4xl font-bold text-white font-serif mb-4">四大核心特色</h2>
          <p class="text-[var(--color-text-muted)] max-w-2xl mx-auto">从种植到采收，从监测到决策，全方位智能化覆盖</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="(feature, idx) in features" :key="idx"
               class="group relative rounded-xl overflow-hidden border border-[var(--color-border)] bg-[var(--color-bg-panel)]/30 backdrop-blur-sm opacity-0 translate-y-8 feature-card-item"
               :class="{ 'is-visible': featureVisible }"
               :style="{ transitionDelay: `${idx * 150}ms` }"
               @mouseenter="hoveredFeature = idx"
               @mouseleave="hoveredFeature = -1">

            <div class="relative h-48 overflow-hidden">
              <img :src="feature.image" :alt="feature.title"
                   class="w-full h-full object-cover transition-all duration-700 ease-out"
                   :class="hoveredFeature === idx ? 'scale-110' : 'scale-100'"
                   style="filter: brightness(0.7) saturate(1.1);" />
              <div class="absolute inset-0 bg-gradient-to-t from-[var(--color-bg-base)] via-transparent to-transparent"></div>
              <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-br from-[var(--color-cyan-glow)]/10 to-transparent"></div>
            </div>

            <div class="p-6 relative">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center mb-4 text-lg"
                   :class="feature.variant === 'gold' ? 'bg-[var(--color-gold)]/10 text-[var(--color-gold)]' :
                           feature.variant === 'jade' ? 'bg-[var(--color-jade)]/10 text-[var(--color-jade)]' :
                           feature.variant === 'cyan' ? 'bg-[var(--color-cyan-dim)] text-[var(--color-cyan-glow)]' :
                           'bg-white/5 text-white'">
                {{ feature.emoji }}
              </div>
              <h3 class="text-lg font-bold text-white mb-2 group-hover:text-[var(--color-cyan-glow)] transition-colors">{{ feature.title }}</h3>
              <p class="text-sm text-[var(--color-text-muted)] leading-relaxed">{{ feature.description }}</p>

              <div class="absolute bottom-0 right-0 w-16 h-16 opacity-0 group-hover:opacity-100 transition-all duration-500">
                <svg viewBox="0 0 64 64" class="w-full h-full">
                  <path d="M64 0v64H0" fill="none" stroke="var(--color-cyan-glow)" stroke-width="0.5" opacity="0.3"/>
                </svg>
              </div>
            </div>
            <div class="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
                 style="box-shadow: inset 0 0 30px rgba(0,255,204,0.08);">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================ -->
    <!-- QUICK LINKS                                 -->
    <!-- ============================================ -->
    <section class="relative py-24 px-6">
      <div class="max-w-5xl mx-auto">
        <div ref="quickLinksHeaderRef" class="text-center mb-16 opacity-0 translate-y-8" :class="{ 'is-visible': quickLinksHeaderVisible }">
          <h2 class="text-3xl md:text-4xl font-bold text-white font-serif mb-4">快速入口</h2>
          <p class="text-[var(--color-text-muted)]">选择您想探索的功能</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="(link, idx) in quickLinks" :key="idx"
               class="group relative rounded-xl overflow-hidden border border-[var(--color-border)] bg-gradient-to-br from-[var(--color-bg-panel)]/50 to-transparent backdrop-blur-sm p-8 cursor-pointer opacity-0 translate-y-8 quick-link-item hover:scale-[1.02] transition-all duration-500"
               :class="{ 'is-visible': quickLinkVisible }"
               :style="{ transitionDelay: `${idx * 150}ms` }"
               @click="navigateTo(link.path)">

            <div class="w-16 h-16 rounded-full flex items-center justify-center mb-6 text-2xl transition-all duration-500 group-hover:scale-110"
                 :class="link.colorClass">
              {{ link.emoji }}
            </div>

            <h3 class="text-xl font-bold text-white mb-2 group-hover:text-[var(--color-cyan-glow)] transition-colors">{{ link.title }}</h3>
            <p class="text-sm text-[var(--color-text-muted)] mb-6">{{ link.description }}</p>

            <div class="flex items-center gap-2 text-sm font-medium transition-all duration-300" :class="link.arrowClass">
              <span>{{ link.cta }}</span>
              <svg class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </div>

            <div class="absolute -inset-1 bg-gradient-to-r from-[var(--color-cyan-glow)]/0 via-[var(--color-cyan-glow)]/0 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-500 rounded-xl blur-lg pointer-events-none"></div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useIntersectionObserver } from '@vueuse/core'
import { useCountUp } from '@/composables/useCountUp'

const router = useRouter()

// ============================================
// Count-up stats
// ============================================
const { count: countSpecies, startCount: startSpecies } = useCountUp(128)
const { count: countArea, startCount: startArea } = useCountUp(256, { delay: 200 })
const { count: countDevices, startCount: startDevices } = useCountUp(1580, { delay: 400 })

const statItems = computed(() => [
  { value: countSpecies.value, unit: '种', label: '覆盖药材品种' },
  { value: countArea.value, unit: '亩', label: '智慧种植面积' },
  { value: countDevices.value, unit: '+', label: '智能设备接入' },
])

// Fix reactivity — use separate refs for the values
import { watch } from 'vue'

// ============================================
// Features
// ============================================
const features = [
  {
    image: '/feature-full-process.webp', emoji: '🌿', title: '全流程化',
    description: '从育苗到采收，全程数字化追踪与管理，实现中药材全生命周期智慧管控。',
    variant: 'jade',
  },
  {
    image: '/feature-data-driven.webp', emoji: '📊', title: '数据驱动',
    description: '多维传感器实时采集，AI算法精准分析，让每一个决策都有数据支撑。',
    variant: 'cyan',
  },
  {
    image: '/feature-precision-ai.webp', emoji: '🎯', title: '精准智能',
    description: '病虫害声学识别、多光谱分析、AI决策建议，精准到每一株药材。',
    variant: 'gold',
  },
  {
    image: '/feature-green-eco.webp', emoji: '♻️', title: '绿色高效',
    description: '智能水肥一体化、精准施药、节水节肥率超23%，绿色可持续发展。',
    variant: 'default',
  },
]

const hoveredFeature = ref(-1)

// ============================================
// Quick Links
// ============================================
const quickLinks = [
  {
    path: '/monitor', emoji: '🛸', title: '在线监测',
    description: '实时查看有棚区与无棚区的环境数据、设备状态和AI决策日志。',
    cta: '进入监测平台',
    colorClass: 'bg-[var(--color-cyan-dim)] text-[var(--color-cyan-glow)]',
    arrowClass: 'text-[var(--color-cyan-glow)]',
  },
  {
    path: '/herbspirit', emoji: '🧓', title: '认识百草通灵',
    description: '与百草通灵对话，获取节气养生建议、本草知识和农事指导。',
    cta: '开始对话',
    colorClass: 'bg-[var(--color-gold)]/10 text-[var(--color-gold)]',
    arrowClass: 'text-[var(--color-gold)]',
  },
  {
    path: '/product', emoji: '📖', title: '产品详情',
    description: '了解项目的四大核心特色与"种管没收"全流程解决方案。',
    cta: '查看详情',
    colorClass: 'bg-white/5 text-white',
    arrowClass: 'text-white',
  },
]

const navigateTo = (path) => { router.push(path) }

// ============================================
// Scroll-triggered animations
// ============================================

// Overview text
const overviewTextRef = ref(null)
const overviewVisible = ref(false)
useIntersectionObserver(overviewTextRef, ([{ isIntersecting }]) => {
  if (isIntersecting) overviewVisible.value = true
}, { threshold: 0.3 })

// Stats + count-up trigger
const statsRef = ref(null)
const statVisible = ref(false)
useIntersectionObserver(statsRef, ([{ isIntersecting }]) => {
  if (isIntersecting) {
    statVisible.value = true
    startSpecies()
    startArea()
    startDevices()
  }
}, { threshold: 0.3 })

// Features header
const featuresHeaderRef = ref(null)
const featuresHeaderVisible = ref(false)
useIntersectionObserver(featuresHeaderRef, ([{ isIntersecting }]) => {
  if (isIntersecting) featuresHeaderVisible.value = true
}, { threshold: 0.3 })

// Features cards — trigger when header comes into view
const featureVisible = ref(false)
watch(featuresHeaderVisible, (v) => { if (v) featureVisible.value = true })

// Quick links header
const quickLinksHeaderRef = ref(null)
const quickLinksHeaderVisible = ref(false)
useIntersectionObserver(quickLinksHeaderRef, ([{ isIntersecting }]) => {
  if (isIntersecting) quickLinksHeaderVisible.value = true
}, { threshold: 0.3 })

// Quick links cards
const quickLinkVisible = ref(false)
watch(quickLinksHeaderVisible, (v) => { if (v) setTimeout(() => { quickLinkVisible.value = true }, 100) })

// ============================================
// Particles
// ============================================
const particleDefs = [
  { top: '15%', left: '10%', size: 4, delay: '0s', duration: '6s', color: '#4ecdc4' },
  { top: '25%', left: '80%', size: 3, delay: '1s', duration: '7s', color: '#c4a86a' },
  { top: '45%', left: '20%', size: 5, delay: '0.5s', duration: '8s', color: '#00ffcc' },
  { top: '60%', left: '70%', size: 3, delay: '2s', duration: '6s', color: '#6b9f6b' },
  { top: '75%', left: '15%', size: 4, delay: '1.5s', duration: '9s', color: '#4ecdc4' },
  { top: '35%', left: '60%', size: 2, delay: '0.8s', duration: '7s', color: '#c4a86a' },
  { top: '55%', left: '85%', size: 3, delay: '2.5s', duration: '5s', color: '#00ffcc' },
  { top: '80%', left: '40%', size: 4, delay: '1.2s', duration: '8s', color: '#6b9f6b' },
  { top: '10%', left: '50%', size: 2, delay: '3s', duration: '6s', color: '#00ffcc' },
  { top: '70%', left: '90%', size: 3, delay: '0.3s', duration: '7s', color: '#c4a86a' },
  { top: '40%', left: '45%', size: 5, delay: '1.8s', duration: '9s', color: '#4ecdc4' },
  { top: '90%', left: '5%', size: 2, delay: '2.2s', duration: '6s', color: '#00ffcc' },
]

const particles = particleDefs.map((p, i) => ({
  key: i,
  style: {
    top: p.top,
    left: p.left,
    width: p.size + 'px',
    height: p.size + 'px',
    backgroundColor: p.color,
    boxShadow: `0 0 ${p.size * 3}px ${p.color}`,
    animation: `float-particle ${p.duration} ease-in-out ${p.delay} infinite alternate`,
  }
}))
</script>

<style scoped>
/* Hero animations */
@keyframes float-particle {
  0% { transform: translateY(0) translateX(0); opacity: 0.08; }
  50% { transform: translateY(-20px) translateX(10px); opacity: 0.15; }
  100% { transform: translateY(5px) translateX(-5px); opacity: 0.08; }
}

@keyframes drift-slow {
  0% { transform: translateX(0) translateY(0) rotate(0deg); }
  25% { transform: translateX(80px) translateY(-30px) rotate(3deg); }
  50% { transform: translateX(160px) translateY(-10px) rotate(5deg); }
  75% { transform: translateX(240px) translateY(-40px) rotate(2deg); }
  100% { transform: translateX(320px) translateY(-20px) rotate(4deg); }
}

@keyframes float-slow {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-15px) scale(1.05); }
}

.animate-drift-slow {
  animation: drift-slow 20s ease-in-out infinite;
}

.animate-float-slow {
  animation: float-slow 5s ease-in-out infinite;
}

.scroll-indicator {
  animation: bounce-down 2s ease-in-out infinite;
}

@keyframes bounce-down {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(8px); }
}

/* Hero staggered reveal */
.animate-hero-item {
  animation: heroFadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes heroFadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Scroll-triggered reveal */
.is-visible {
  animation: revealUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes revealUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.opacity-0 {
  opacity: 0;
}

.translate-y-8 {
  transform: translateY(30px);
}
</style>
