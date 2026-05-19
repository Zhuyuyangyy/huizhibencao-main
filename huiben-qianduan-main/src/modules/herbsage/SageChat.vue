<template>
  <div class="flex flex-col h-full">
    <!-- Messages area -->
    <div ref="chatRef" class="flex-1 overflow-y-auto custom-scrollbar px-5 py-4">
      <div class="max-w-3xl mx-auto space-y-1">
        <div v-for="(msg, mi) in messages" :key="msg.id"
             class="flex items-end gap-3 message-enter"
             :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
             :style="{ animationDelay: `${mi * 0.05}s` }">

          <!-- Sage avatar -->
          <div v-if="msg.role === 'sage'"
               class="w-8 h-8 rounded-lg overflow-hidden border border-[var(--color-gold)]/20 shrink-0 shadow-lg shadow-black/30 mb-1">
            <img src="/laozu-portrait.png" alt="百草通灵" class="w-full h-full object-cover" />
          </div>

          <div class="max-w-[75%] group">
            <!-- Message bubble -->
            <div class="relative px-4 py-3 text-sm leading-relaxed"
                 :class="msg.role === 'sage'
                   ? 'scroll-bubble-sage'
                   : 'scroll-bubble-user'">
              <!-- Decorative top accent -->
              <div v-if="msg.role === 'sage'"
                   class="absolute -top-px left-4 right-[70%] h-px bg-gradient-to-r from-[var(--color-gold)]/40 to-transparent">
              </div>
              <div v-else
                   class="absolute -top-px right-4 left-[70%] h-px bg-gradient-to-l from-[var(--color-cyan-glow)]/40 to-transparent">
              </div>

              <p class="whitespace-pre-line" :class="msg.role === 'sage' ? 'text-gray-200' : 'text-white/90'">
                {{ msg.content }}
              </p>
            </div>

            <!-- Timestamp -->
            <div class="text-[9px] text-gray-700 mt-1 px-1 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                 :class="msg.role === 'sage' ? 'text-left' : 'text-right'">
              {{ formatTime(msg.timestamp) }}
            </div>
          </div>

          <!-- User avatar placeholder -->
          <div v-if="msg.role === 'user'"
               class="w-8 h-8 rounded-lg shrink-0 mb-1 flex items-center justify-center
                      bg-gradient-to-br from-[var(--color-cyan-glow)]/20 to-[var(--color-jade)]/10
                      border border-[var(--color-border)]">
            <svg class="w-4 h-4 text-[var(--color-cyan-glow)]/60" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        </div>

        <!-- Typing indicator -->
        <div v-if="isTyping" class="flex items-end gap-3 message-enter">
          <div class="w-8 h-8 rounded-lg overflow-hidden border border-[var(--color-gold)]/20 shrink-0 shadow-lg shadow-black/30 mb-1">
            <img src="/laozu-portrait.png" alt="百草通灵" class="w-full h-full object-cover" />
          </div>
          <div class="scroll-bubble-sage px-4 py-3">
            <div class="flex gap-1.5">
              <span class="w-2 h-2 rounded-full bg-[var(--color-cyan-glow)]/60 animate-bounce" style="animation-delay: 0s"></span>
              <span class="w-2 h-2 rounded-full bg-[var(--color-cyan-glow)]/60 animate-bounce" style="animation-delay: 0.15s"></span>
              <span class="w-2 h-2 rounded-full bg-[var(--color-cyan-glow)]/60 animate-bounce" style="animation-delay: 0.3s"></span>
            </div>
          </div>
        </div>

        <!-- Quick questions suggestions -->
        <div v-if="showSuggestions" class="flex flex-wrap gap-2 pt-4 pb-2 max-w-[80%]">
          <button v-for="q in quickQuestions" :key="q.id"
                  @click="ask(q.text, q.type)"
                  class="group relative px-3.5 py-2 rounded-lg text-xs transition-all duration-300 overflow-hidden"
                  :class="clickedTip === q.id
                    ? 'border border-[var(--color-cyan-glow)] text-[var(--color-cyan-glow)]'
                    : 'border border-[var(--color-border)] text-gray-400 hover:text-white hover:border-[var(--color-border-strong)]'">
            <!-- Hover glow -->
            <div class="absolute inset-0 bg-gradient-to-r from-[var(--color-cyan-glow)]/0 via-[var(--color-cyan-glow)]/5 to-[var(--color-cyan-glow)]/0
                        opacity-0 group-hover:opacity-100 transition-opacity duration-500
                        -translate-x-full group-hover:translate-x-full"
                 style="transition: all 0.6s ease;">
            </div>
            <span class="relative z-10">{{ q.text }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Input bar -->
    <div class="shrink-0 px-5 py-3 border-t border-[var(--color-border)] bg-gradient-to-t from-[var(--color-bg-base)] to-transparent">
      <div class="max-w-3xl mx-auto">
        <div class="flex items-center gap-2">
          <div class="flex-1 relative">
            <input ref="inputRef" v-model="inputText"
                   @keyup.enter="sendMessage"
                   placeholder="向百草通灵请教..."
                   class="w-full px-4 py-2.5 rounded-xl border bg-black/40 text-sm text-white placeholder-gray-600 outline-none transition-all duration-300"
                   :class="inputText.trim()
                     ? 'border-[var(--color-border-strong)] focus:border-[var(--color-cyan-glow)]/50 focus:shadow-[0_0_20px_rgba(0,255,204,0.05)]'
                     : 'border-[var(--color-border)] focus:border-[var(--color-cyan-glow)]/30'" />
          </div>
          <button @click="sendMessage"
                  class="px-4 py-2.5 rounded-xl transition-all duration-300 font-medium text-xs shrink-0"
                  :class="inputText.trim()
                    ? 'bg-gradient-to-r from-[var(--color-cyan-glow)] to-[var(--color-jade-light)] text-[var(--color-bg-base)] shadow-[0_0_15px_rgba(0,255,204,0.15)] hover:shadow-[0_0_25px_rgba(0,255,204,0.25)]'
                    : 'bg-white/5 text-gray-500 border border-[var(--color-border)]'">
            <span class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              发送
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'

const props = defineProps({
  messages: { type: Array, required: true },
  isTyping: { type: Boolean, default: false },
  quickQuestions: { type: Array, default: () => [] },
  expression: { type: String, default: 'happy' },
})

const emit = defineEmits(['ask'])
const inputText = ref('')
const chatRef = ref(null)
const inputRef = ref(null)
const clickedTip = ref(null)

const showSuggestions = computed(() => {
  return props.messages.length === 1 && props.messages[0].role === 'sage' && !props.isTyping
})

const sendMessage = () => {
  const text = inputText.value.trim()
  if (!text) return
  emit('ask', text, 'default')
  inputText.value = ''
  clickedTip.value = null
  inputRef.value?.focus()
}

const ask = (text, type) => {
  clickedTip.value = text
  emit('ask', text, type)
  setTimeout(() => { clickedTip.value = null }, 600)
}

const formatTime = (ts) => {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

watch(() => props.messages.length, async () => {
  await nextTick()
  if (chatRef.value) {
    chatRef.value.scrollTo({ top: chatRef.value.scrollHeight, behavior: 'smooth' })
  }
})
</script>

<style scoped>
/* Scroll-like bubble for sage messages */
.scroll-bubble-sage {
  background: linear-gradient(135deg, rgba(4, 26, 51, 0.9) 0%, rgba(10, 20, 35, 0.9) 100%);
  border: 1px solid rgba(0, 255, 204, 0.12);
  border-left: 2px solid rgba(196, 168, 106, 0.4);
  border-radius: 4px 12px 12px 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2),
              inset 0 0 30px rgba(0, 255, 204, 0.02);
}

/* Scroll-like bubble for user messages */
.scroll-bubble-user {
  background: linear-gradient(135deg, rgba(0, 255, 204, 0.08) 0%, rgba(45, 138, 110, 0.06) 100%);
  border: 1px solid rgba(0, 255, 204, 0.15);
  border-right: 2px solid rgba(0, 255, 204, 0.3);
  border-radius: 12px 4px 4px 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

/* Message entrance animation */
.message-enter {
  animation: messageSlide 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(12px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
