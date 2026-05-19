<template>
  <footer class="relative z-10 border-t border-[var(--color-border)] bg-[var(--color-bg-base)]/90 backdrop-blur-sm">
    <div class="max-w-7xl mx-auto px-6 py-10">
      <!-- Main footer grid -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">

        <!-- Brand column -->
        <div class="md:col-span-1">
          <div class="flex items-center gap-2.5 mb-3">
            <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-[var(--color-jade)] to-[var(--color-cyan-glow)] flex items-center justify-center">
              <span class="text-[var(--color-bg-base)] font-bold text-base font-serif">慧</span>
            </div>
            <div>
              <h3 class="text-base font-bold text-white font-serif tracking-wider">慧植本草</h3>
              <p class="text-[10px] text-[var(--color-text-secondary)] tracking-[0.15em]">方寸灵畦</p>
            </div>
          </div>
          <p class="text-sm text-[var(--color-text-muted)] leading-relaxed max-w-xs">
            AI赋能道地药材，数字振兴乡土本草。智慧农业与传统中医药的深度融合。
          </p>
        </div>

        <!-- Quick links -->
        <div>
          <h4 class="text-sm font-bold text-white mb-4 tracking-wider">快速导航</h4>
          <ul class="space-y-2.5">
            <li v-for="link in quickLinks" :key="link.path">
              <router-link :to="link.path" class="text-sm text-[var(--color-text-muted)] hover:text-[var(--color-cyan-glow)] transition-colors duration-200">
                {{ link.label }}
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Contact info -->
        <div>
          <h4 class="text-sm font-bold text-white mb-4 tracking-wider">联系方式</h4>
          <ul class="space-y-2.5 text-sm text-[var(--color-text-muted)]">
            <li class="flex items-start gap-2">
              <svg class="w-4 h-4 mt-0.5 text-[var(--color-cyan-glow)] shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>安徽省亳州市谯城区<br>中药材智慧种植示范区</span>
            </li>
            <li class="flex items-center gap-2">
              <svg class="w-4 h-4 text-[var(--color-cyan-glow)] shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>contact@herbwise.agri</span>
            </li>
          </ul>
        </div>

        <!-- QR / social -->
        <div>
          <h4 class="text-sm font-bold text-white mb-4 tracking-wider">关注我们</h4>
          <div class="flex gap-3">
            <div class="w-20 h-20 rounded-lg border border-[var(--color-border)] bg-white/5 flex items-center justify-center">
              <div class="text-center">
                <svg class="w-8 h-8 mx-auto text-[var(--color-text-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
                </svg>
                <p class="text-[10px] text-[var(--color-text-muted)] mt-1">公众号</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Divider -->
      <div class="h-px bg-gradient-to-r from-transparent via-[var(--color-border)] to-transparent mb-6"></div>

      <!-- Bottom bar -->
      <div class="flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-[var(--color-text-muted)]">
        <p>© 2025 慧植本草 · 方寸灵畦. All rights reserved.</p>
        <div class="flex items-center gap-4">
          <span class="hover:text-[var(--color-text-secondary)] transition-colors cursor-pointer">隐私政策</span>
          <span class="hover:text-[var(--color-text-secondary)] transition-colors cursor-pointer">使用条款</span>
          <span class="flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-[var(--color-alert-success)] shadow-[0_0_6px_rgba(34,197,94,0.5)]"></span>
            系统 v3.0
          </span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const quickLinks = [
  { path: '/', label: '首页' },
  { path: '/monitor', label: '在线监测' },
  { path: '/product', label: '产品简介' },
  { path: '/herbspirit', label: '本草精灵' },
  { path: '/contact', label: '联系我们' },
]
</script>
