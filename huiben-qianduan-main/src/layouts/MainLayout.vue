<template>
  <div class="min-h-screen flex flex-col relative bg-[var(--color-bg-base)]">
    <!-- Background ambient glow -->
    <div class="fixed top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[var(--color-cyan-glow)] rounded-full blur-[150px] opacity-[0.03] pointer-events-none"></div>
    <div class="fixed bottom-0 right-0 w-[500px] h-[500px] bg-[var(--color-jade)] rounded-full blur-[120px] opacity-[0.02] pointer-events-none"></div>

    <!-- NavBar -->
    <NavBar />

    <!-- Main Content -->
    <main class="flex-1 relative z-10 h-full">
      <slot />
    </main>

    <!-- Footer (hidden on pages that set meta.hideFooter) -->
    <Footer v-if="!hideFooter" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import Footer from '@/components/Footer.vue'

const route = useRoute()
const hideFooter = computed(() => route.meta?.hideFooter === true)
</script>
