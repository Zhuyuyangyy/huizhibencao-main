<template>
  <nav class="fixed top-0 left-0 right-0 z-50 px-6 py-3"
       :class="{ 'bg-[var(--color-bg-panel)] backdrop-blur-xl border-b border-[var(--color-border)]': scrolled,
                'bg-transparent': !scrolled }"
       style="transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-3 group">
        <div class="relative">
          <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-[var(--color-jade)] to-[var(--color-cyan-glow)] flex items-center justify-center shadow-[0_0_15px_rgba(0,255,204,0.3)] group-hover:shadow-[0_0_25px_rgba(0,255,204,0.5)] transition-shadow duration-300">
            <span class="text-[var(--color-bg-base)] font-bold text-lg font-serif">慧</span>
          </div>
          <div class="absolute -inset-1 rounded-lg bg-gradient-to-br from-[var(--color-cyan-glow)]/0 to-[var(--color-jade)]/0 group-hover:from-[var(--color-cyan-glow)]/20 group-hover:to-[var(--color-jade)]/20 transition-all duration-500 -z-10 blur-sm"></div>
        </div>
        <div class="hidden sm:block">
          <h1 class="text-lg font-bold text-white font-serif tracking-wider">慧植本草</h1>
          <p class="text-[10px] text-[var(--color-text-secondary)] tracking-[0.15em] uppercase">方寸灵畦</p>
        </div>
      </router-link>

      <!-- Navigation Items -->
      <div class="hidden md:flex items-center gap-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="relative px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 group"
          :class="isActive(item.path)
            ? 'text-[var(--color-cyan-glow)]'
            : 'text-[var(--color-text-secondary)] hover:text-white hover:bg-white/5'"
        >
          <span class="relative z-10">{{ item.label }}</span>
          <!-- Active indicator -->
          <div v-if="isActive(item.path)"
               class="absolute inset-0 rounded-lg bg-gradient-to-r from-[var(--color-cyan-glow)]/10 to-transparent border border-[var(--color-border)]">
          </div>
          <div v-if="isActive(item.path)"
               class="absolute -bottom-px left-[20%] right-[20%] h-[2px] bg-gradient-to-r from-transparent via-[var(--color-cyan-glow)] to-transparent shadow-[0_0_8px_rgba(0,255,204,0.5)]">
          </div>
        </router-link>
      </div>

      <!-- Right side: status -->
      <div class="flex items-center gap-4">
        <div class="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-[var(--color-cyan-dim)] border border-[var(--color-border)]">
          <div class="w-2 h-2 rounded-full bg-[var(--color-alert-success)] shadow-[0_0_8px_rgba(34,197,94,0.5)] animate-pulse"></div>
          <span class="text-xs text-[var(--color-text-secondary)]">系统运行中</span>
        </div>

        <!-- Mobile menu toggle -->
        <button @click="mobileOpen = !mobileOpen" class="md:hidden p-2 rounded-lg text-[var(--color-text-secondary)] hover:text-white hover:bg-white/5 transition-colors">
          <svg v-if="!mobileOpen" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <transition name="slide-down">
      <div v-if="mobileOpen" class="md:hidden mt-4 pb-4 border-t border-[var(--color-border)] pt-4">
        <div class="flex flex-col gap-1">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            @click="mobileOpen = false"
            class="px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200"
            :class="isActive(item.path)
              ? 'text-[var(--color-cyan-glow)] bg-[var(--color-cyan-dim)] border-l-2 border-[var(--color-cyan-glow)]'
              : 'text-[var(--color-text-secondary)] hover:text-white hover:bg-white/5'"
          >
            {{ item.label }}
          </router-link>
        </div>
      </div>
    </transition>
  </nav>

  <!-- Spacer for fixed nav -->
  <div class="h-[72px]"></div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const scrolled = ref(false)
const mobileOpen = ref(false)

const navItems = [
  { path: '/', label: '首页' },
  { path: '/monitor', label: '在线监测' },
  { path: '/product', label: '产品简介' },
  { path: '/herbspirit', label: '本草精灵' },
  { path: '/contact', label: '联系我们' },
]

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

let scrollHandler = null
onMounted(() => {
  scrollHandler = () => { scrolled.value = window.scrollY > 20 }
  window.addEventListener('scroll', scrollHandler, { passive: true })
})
onUnmounted(() => {
  if (scrollHandler) window.removeEventListener('scroll', scrollHandler)
})
</script>

<style scoped>
.slide-down-enter-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-down-leave-active { transition: all 0.2s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-10px); }
</style>
