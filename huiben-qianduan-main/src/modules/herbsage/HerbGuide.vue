<template>
  <div>
    <!-- Filters -->
    <div class="flex flex-wrap gap-4 mb-6">
      <div v-for="(filter, fi) in filters" :key="fi" class="flex items-center gap-2">
        <span class="text-xs text-gray-500 font-medium tracking-wider">{{ filter.label }}</span>
        <div class="flex gap-1">
          <button v-for="opt in filter.options" :key="opt"
                  @click="toggleFilter(fi, opt)"
                  class="px-2.5 py-1 rounded text-xs transition-all duration-200"
                  :class="isFilterActive(fi, opt)
                    ? 'bg-[var(--color-cyan-dim)] text-[var(--color-cyan-glow)] border border-[var(--color-border-strong)] shadow-[0_0_8px_rgba(0,255,204,0.05)]'
                    : 'text-gray-500 border border-[var(--color-border)] hover:text-white hover:border-[var(--color-border-strong)] bg-black/20'">
            {{ opt }}
          </button>
        </div>
      </div>
      <button v-if="hasActiveFilters" @click="clearFilters"
              class="px-2.5 py-1 rounded text-xs text-gray-500 hover:text-white border border-transparent hover:border-[var(--color-border)] transition-all">
        清除
      </button>
    </div>

    <!-- Herb grid -->
    <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-3">
      <div v-for="herb in filteredHerbs" :key="herb.id"
           class="herb-card group rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-panel)]/20 overflow-hidden cursor-pointer transition-all duration-400 hover:-translate-y-1"
           @click="selectHerb(herb)">
        <!-- Image area with decorative frame -->
        <div class="relative h-24 overflow-hidden">
          <!-- Decorative top corners -->
          <div class="absolute top-0 left-0 w-6 h-6 border-t border-l border-[var(--color-gold)]/20 z-10 rounded-tl"></div>
          <div class="absolute top-0 right-0 w-6 h-6 border-t border-r border-[var(--color-gold)]/20 z-10 rounded-tr"></div>

          <div class="w-full h-full bg-gradient-to-b from-black/40 to-black/10 flex items-center justify-center p-2">
            <img :src="herb.image" :alt="herb.name"
                 class="w-full h-full object-contain transition-all duration-500 group-hover:scale-110 drop-shadow-[0_4px_12px_rgba(0,0,0,0.4)]" />
          </div>

          <!-- Bottom fade -->
          <div class="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-[var(--color-bg-panel)]/80 to-transparent"></div>
        </div>

        <!-- Info area -->
        <div class="p-3.5">
          <h4 class="text-sm font-bold text-white group-hover:text-[var(--color-cyan-glow)] transition-colors duration-300">{{ herb.name }}</h4>
          <p class="text-[10px] text-gray-500 italic mt-0.5">{{ herb.latin }}</p>
          <div class="flex items-center gap-2 mt-2">
            <span class="text-[10px] px-1.5 py-0.5 rounded border border-[var(--color-border)] text-gray-400 bg-black/30">{{ herb.nature }}</span>
            <span class="text-[10px] text-gray-500">{{ herb.flavors.join('、') }}</span>
          </div>
          <!-- Category tag -->
          <div class="mt-1.5">
            <span class="text-[9px] px-1.5 py-0.5 rounded-full bg-[var(--color-cyan-dim)]/50 text-[var(--color-cyan-glow)]/70">{{ herb.category }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="filteredHerbs.length === 0"
         class="text-center py-16">
      <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gray-500/10 border border-gray-500/20 flex items-center justify-center">
        <svg class="w-7 h-7 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <p class="text-sm text-gray-500">没有匹配的药材</p>
      <button @click="clearFilters" class="mt-2 text-xs text-[var(--color-cyan-glow)] hover:underline">清除筛选</button>
    </div>

    <!-- Detail modal -->
    <Teleport to="body">
      <transition name="modal-enter">
        <div v-if="detailHerb" class="fixed inset-0 z-[100] flex items-center justify-center p-4"
             @click.self="detailHerb = null">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/70 backdrop-blur-sm"></div>

          <!-- Modal -->
          <div class="relative w-[520px] max-h-[85vh] overflow-y-auto rounded-2xl border border-[var(--color-border-strong)] bg-gradient-to-b from-[#0d1a28] to-[#081218] p-6 shadow-2xl custom-scrollbar">
            <!-- Decorative top border -->
            <div class="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-[var(--color-gold)]/30 to-transparent"></div>

            <!-- Header -->
            <div class="flex justify-between items-start mb-6">
              <div class="flex items-center gap-4">
                <div class="w-20 h-20 rounded-xl bg-gradient-to-b from-black/40 to-black/20 border border-[var(--color-border)] overflow-hidden flex items-center justify-center p-2">
                  <img :src="detailHerb.image" :alt="detailHerb.name" class="w-full h-full object-contain" />
                </div>
                <div>
                  <h3 class="text-xl font-bold text-white font-serif">{{ detailHerb.name }}</h3>
                  <p class="text-xs text-gray-500 italic mt-0.5">{{ detailHerb.latin }}</p>
                  <span class="inline-block mt-1 text-[10px] px-2 py-0.5 rounded-full bg-[var(--color-cyan-dim)]/50 text-[var(--color-cyan-glow)]/70 border border-[var(--color-border)]">
                    {{ detailHerb.category }}
                  </span>
                </div>
              </div>
              <button @click="detailHerb = null"
                      class="w-8 h-8 rounded-lg flex items-center justify-center text-gray-500 hover:text-white hover:bg-white/5 transition-all">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Properties tags -->
            <div class="flex flex-wrap gap-2 mb-5">
              <span class="px-3 py-1 rounded-lg border border-[var(--color-border)] text-xs text-gray-300 bg-black/30">{{ detailHerb.nature }}</span>
              <span v-for="f in detailHerb.flavors" :key="f"
                    class="px-3 py-1 rounded-lg border border-[var(--color-border)] text-xs text-gray-300 bg-black/30">{{ f }}</span>
              <span v-for="m in detailHerb.meridians" :key="m"
                    class="px-3 py-1 rounded-full text-[10px] bg-[var(--color-cyan-dim)] text-[var(--color-cyan-glow)] border border-[var(--color-border)]">
                归{{ m }}
              </span>
            </div>

            <!-- Content sections -->
            <div class="space-y-3 text-sm">
              <div class="p-4 rounded-xl border border-[var(--color-border)] bg-black/30">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-[10px] text-[var(--color-cyan-glow)] uppercase tracking-wider font-medium">功效</span>
                  <span class="flex-1 h-px bg-gradient-to-r from-[var(--color-cyan-glow)]/20 to-transparent"></span>
                </div>
                <p class="text-gray-200 leading-relaxed">{{ detailHerb.efficacy }}</p>
              </div>
              <div class="p-4 rounded-xl border border-[var(--color-border)] bg-black/30">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-[10px] text-[var(--color-gold)] uppercase tracking-wider font-medium">用法用量</span>
                  <span class="flex-1 h-px bg-gradient-to-r from-[var(--color-gold)]/20 to-transparent"></span>
                </div>
                <p class="text-gray-300 leading-relaxed">{{ detailHerb.usage }}</p>
              </div>
              <div class="p-4 rounded-xl border border-yellow-500/20 bg-gradient-to-br from-yellow-500/5 to-transparent">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-[10px] text-yellow-400 uppercase tracking-wider font-medium">⚠️ 注意事项</span>
                  <span class="flex-1 h-px bg-gradient-to-r from-yellow-500/20 to-transparent"></span>
                </div>
                <p class="text-yellow-200/80 leading-relaxed">{{ detailHerb.caution }}</p>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { herbs, natureOptions, flavorOptions, meridianOptions } from '@/data/herbs'

const activeFilters = ref({ nature: [], flavor: [], meridian: [] })
const detailHerb = ref(null)

const filters = [
  { label: '四气', key: 'nature', options: natureOptions },
  { label: '五味', key: 'flavor', options: flavorOptions },
  { label: '归经', key: 'meridian', options: meridianOptions },
]

const hasActiveFilters = computed(() => {
  return Object.values(activeFilters.value).some(arr => arr.length > 0)
})

const toggleFilter = (fi, opt) => {
  const key = filters[fi].key
  const arr = activeFilters.value[key]
  const idx = arr.indexOf(opt)
  if (idx >= 0) arr.splice(idx, 1)
  else arr.push(opt)
}

const isFilterActive = (fi, opt) => {
  return activeFilters.value[filters[fi].key].includes(opt)
}

const clearFilters = () => {
  activeFilters.value = { nature: [], flavor: [], meridian: [] }
}

const filteredHerbs = computed(() => {
  return herbs.filter(h => {
    const nf = activeFilters.value.nature
    const ff = activeFilters.value.flavor
    const mf = activeFilters.value.meridian
    if (nf.length && !nf.includes(h.nature)) return false
    if (ff.length && !ff.some(f => h.flavors.includes(f))) return false
    if (mf.length && !mf.some(m => h.meridians.includes(m))) return false
    return true
  })
})

const selectHerb = (herb) => { detailHerb.value = herb }
</script>

<style scoped>
.herb-card {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}
.herb-card:hover {
  border-color: rgba(0, 255, 204, 0.3);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3),
              0 0 20px rgba(0, 255, 204, 0.05);
}

/* Modal transitions */
.modal-enter-enter-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.modal-enter-leave-active {
  transition: all 0.2s ease;
}
.modal-enter-enter-from,
.modal-enter-leave-to {
  opacity: 0;
}
.modal-enter-enter-active > div:last-child {
  animation: modal-scale 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes modal-scale {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>
