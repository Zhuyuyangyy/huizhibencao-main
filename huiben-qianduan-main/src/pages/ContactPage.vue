<template>
  <div>
    <!-- ===== HERO ===== -->
    <section class="relative h-[340px] md:h-[400px] overflow-hidden">
      <!-- Background image -->
      <div class="absolute inset-0 bg-cover bg-center"
           style="background-image: url('/contact-bg.webp');">
      </div>
      <!-- Dark overlay -->
      <div class="absolute inset-0 bg-gradient-to-r from-[var(--color-bg-base)]/90 via-[var(--color-bg-base)]/60 to-transparent"></div>
      <div class="absolute inset-0 bg-gradient-to-t from-[var(--color-bg-base)] to-transparent opacity-60"></div>

      <!-- Decorative glow -->
      <div class="absolute top-1/2 left-1/4 w-[300px] h-[300px] rounded-full bg-[var(--color-jade)] blur-[120px] opacity-[0.06]"></div>

      <!-- Content -->
      <div class="relative z-10 h-full max-w-7xl mx-auto px-6 flex flex-col justify-center">
        <div class="max-w-xl">
          <div class="flex items-center gap-3 mb-4">
            <span class="w-8 h-px bg-[var(--color-cyan-glow)]/60"></span>
            <span class="text-xs text-[var(--color-cyan-glow)] uppercase tracking-[0.2em] font-medium">Contact</span>
          </div>
          <h1 class="text-4xl md:text-5xl font-bold text-white font-serif mb-3">联系我们</h1>
          <p class="text-[var(--color-text-secondary)] text-sm md:text-base leading-relaxed max-w-lg">
            期待与您携手，用科技传承本草智慧。<br>无论合作、咨询还是建议，我们随时倾听。
          </p>
        </div>
      </div>
    </section>

    <!-- ===== MAIN CONTENT ===== -->
    <section class="max-w-7xl mx-auto px-6 py-16">
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-12">
        <!-- Left: Contact Info (2/5) -->
        <div class="lg:col-span-2 space-y-10">
          <!-- Info cards -->
          <div class="space-y-4">
            <div v-for="(item, idx) in contactInfo" :key="idx"
                 class="group flex items-start gap-4 p-5 rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-panel)]/30 hover:bg-[var(--color-bg-panel)]/50 transition-all duration-300">
              <div class="w-11 h-11 rounded-xl flex items-center justify-center shrink-0 text-lg transition-all duration-300 group-hover:scale-110"
                   :style="{ background: item.bg, border: `1px solid ${item.border}` }">
                <span>{{ item.icon }}</span>
              </div>
              <div class="min-w-0">
                <div class="text-xs text-gray-500 font-medium uppercase tracking-wider mb-0.5">{{ item.label }}</div>
                <div class="text-sm text-white" v-html="item.value"></div>
              </div>
            </div>
          </div>

          <!-- QR Code -->
          <div class="p-6 rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-panel)]/20 text-center">
            <div class="w-28 h-28 mx-auto mb-3 rounded-xl border border-[var(--color-border)] bg-black/40 flex items-center justify-center">
              <svg class="w-16 h-16 text-[var(--color-cyan-glow)]/30" viewBox="0 0 100 100" fill="currentColor">
                <rect x="10" y="10" width="30" height="30" rx="3"/>
                <rect x="55" y="10" width="10" height="10" rx="1"/>
                <rect x="10" y="55" width="10" height="10" rx="1"/>
                <rect x="25" y="55" width="15" height="15" rx="1"/>
                <rect x="55" y="25" width="15" height="15" rx="1"/>
                <rect x="75" y="25" width="15" height="15" rx="1"/>
                <rect x="55" y="55" width="10" height="10" rx="1"/>
                <rect x="70" y="55" width="20" height="20" rx="1"/>
                <rect x="55" y="75" width="10" height="15" rx="1"/>
                <rect x="75" y="80" width="15" height="10" rx="1"/>
                <rect x="25" y="75" width="15" height="15" rx="1"/>
                <rect x="10" y="75" width="10" height="10" rx="1"/>
              </svg>
            </div>
            <p class="text-xs text-gray-500 mb-1">扫码关注公众号</p>
            <p class="text-[10px] text-gray-600">慧植本草 · 方寸灵畦</p>
          </div>
        </div>

        <!-- Right: Contact Form (3/5) -->
        <div class="lg:col-span-3">
          <div class="p-8 rounded-2xl border border-[var(--color-border)] bg-gradient-to-br from-[var(--color-bg-panel)]/40 to-transparent backdrop-blur-sm">
            <!-- Form header -->
            <div class="mb-8">
              <h2 class="text-xl font-bold text-white font-serif mb-2">发送留言</h2>
              <p class="text-sm text-gray-500">请填写以下信息，我们会在1-2个工作日内回复您</p>
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-5">
              <!-- Name + Phone row -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs text-gray-500 font-medium mb-1.5">姓名 <span class="text-red-400">*</span></label>
                  <input v-model="form.name" type="text" placeholder="请输入姓名"
                         class="w-full px-4 py-2.5 rounded-xl border bg-black/40 text-sm text-white placeholder-gray-600 outline-none transition-all duration-200"
                         :class="formErrors.name ? 'border-red-400/50 focus:border-red-400/70' : 'border-[var(--color-border)] focus:border-[var(--color-cyan-glow)]/30'"
                         @blur="validateField('name')" />
                  <p v-if="formErrors.name" class="text-[10px] text-red-400 mt-1">{{ formErrors.name }}</p>
                </div>
                <div>
                  <label class="block text-xs text-gray-500 font-medium mb-1.5">电话</label>
                  <input v-model="form.phone" type="tel" placeholder="请输入电话"
                         class="w-full px-4 py-2.5 rounded-xl border border-[var(--color-border)] bg-black/40 text-sm text-white placeholder-gray-600 outline-none focus:border-[var(--color-cyan-glow)]/30 transition-all duration-200" />
                </div>
              </div>

              <!-- Email -->
              <div>
                <label class="block text-xs text-gray-500 font-medium mb-1.5">邮箱 <span class="text-red-400">*</span></label>
                <input v-model="form.email" type="email" placeholder="请输入邮箱地址"
                       class="w-full px-4 py-2.5 rounded-xl border bg-black/40 text-sm text-white placeholder-gray-600 outline-none transition-all duration-200"
                       :class="formErrors.email ? 'border-red-400/50 focus:border-red-400/70' : 'border-[var(--color-border)] focus:border-[var(--color-cyan-glow)]/30'"
                       @blur="validateField('email')" />
                <p v-if="formErrors.email" class="text-[10px] text-red-400 mt-1">{{ formErrors.email }}</p>
              </div>

              <!-- Message -->
              <div>
                <label class="block text-xs text-gray-500 font-medium mb-1.5">留言内容 <span class="text-red-400">*</span></label>
                <textarea v-model="form.message" rows="4" placeholder="请写下您的留言..."
                          class="w-full px-4 py-2.5 rounded-xl border bg-black/40 text-sm text-white placeholder-gray-600 outline-none resize-none transition-all duration-200"
                          :class="formErrors.message ? 'border-red-400/50 focus:border-red-400/70' : 'border-[var(--color-border)] focus:border-[var(--color-cyan-glow)]/30'"
                          @blur="validateField('message')"></textarea>
                <p v-if="formErrors.message" class="text-[10px] text-red-400 mt-1">{{ formErrors.message }}</p>
              </div>

              <!-- Submit -->
              <div class="flex items-center gap-4 pt-2">
                <button type="submit" :disabled="submitting"
                        class="px-8 py-2.5 rounded-xl bg-gradient-to-r from-[var(--color-cyan-glow)] to-[var(--color-jade-light)] text-[var(--color-bg-base)] font-bold text-sm transition-all duration-300 hover:shadow-[0_0_25px_rgba(0,255,204,0.25)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2">
                  <svg v-if="submitting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  <span>{{ submitting ? '发送中...' : '发送留言' }}</span>
                  <svg v-if="!submitting" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>

                <transition name="fade">
                  <span v-if="submitted" class="text-sm text-[var(--color-cyan-glow)] flex items-center gap-1.5">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    感谢您的留言，本灵已收到！
                  </span>
                </transition>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const form = reactive({
  name: '',
  email: '',
  phone: '',
  message: '',
})

const formErrors = reactive({
  name: '',
  email: '',
  message: '',
})

const submitting = ref(false)
const submitted = ref(false)

const contactInfo = [
  {
    icon: '📍',
    label: '地址',
    value: '安徽省亳州市谯城区<br>中药材交易中心旁',
    bg: 'rgba(0,255,204,0.08)',
    border: 'rgba(0,255,204,0.2)',
  },
  {
    icon: '📞',
    label: '电话',
    value: '+86 0876-XXX-XXXX',
    bg: 'rgba(196,168,106,0.08)',
    border: 'rgba(196,168,106,0.2)',
  },
  {
    icon: '✉️',
    label: '邮箱',
    value: 'contact@huizhibencao.cn',
    bg: 'rgba(0,255,204,0.08)',
    border: 'rgba(0,255,204,0.2)',
  },
  {
    icon: '🕐',
    label: '工作时间',
    value: '周一至周五 9:00 - 18:00',
    bg: 'rgba(78,205,196,0.08)',
    border: 'rgba(78,205,196,0.2)',
  },
]

const validateField = (field) => {
  if (field === 'name') {
    formErrors.name = form.name.trim().length < 2 ? '请输入姓名（至少2个字符）' : ''
  }
  if (field === 'email') {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    formErrors.email = !re.test(form.email) ? '请输入有效的邮箱地址' : ''
  }
  if (field === 'message') {
    formErrors.message = form.message.trim().length < 5 ? '留言内容至少5个字符' : ''
  }
}

const validate = () => {
  validateField('name')
  validateField('email')
  validateField('message')
  return !formErrors.name && !formErrors.email && !formErrors.message
}

const handleSubmit = async () => {
  if (!validate()) return
  submitting.value = true
  // Simulate send
  await new Promise(r => setTimeout(r, 1500))
  submitting.value = false
  submitted.value = true
  Object.assign(form, { name: '', email: '', phone: '', message: '' })
  setTimeout(() => { submitted.value = false }, 4000)
}
</script>
