<template>
  <div class="relative min-h-[calc(100vh-72px)] overflow-hidden bg-[#060504] text-[#e6cfaa]">
    <div class="absolute inset-0">
      <div
        class="absolute inset-0 scale-105 bg-cover bg-center"
        style="background-image: url('/bencaotujian.png');"
      ></div>
      <div class="absolute inset-0 bg-[rgba(7,5,3,0.84)]"></div>
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(184,133,57,0.16),transparent_32%)]"></div>
      <div class="absolute inset-0 bg-[linear-gradient(120deg,rgba(6,5,4,0.9)_0%,rgba(6,5,4,0.68)_38%,rgba(6,5,4,0.82)_100%)]"></div>
    </div>

    <div class="relative z-10 mx-auto w-[min(1820px,calc(100vw-20px))] px-2 py-5 md:w-[min(1880px,calc(100vw-36px))] md:px-3 md:py-7">
      <div class="grid gap-5 2xl:grid-cols-[272px_minmax(0,1fr)]">
        <aside class="flex flex-col gap-6">
          <div class="rounded-[24px] border border-[rgba(186,139,72,0.16)] bg-[rgba(10,8,6,0.72)] p-4 shadow-[0_24px_60px_rgba(0,0,0,0.24)] backdrop-blur-sm">
            <button
              v-for="item in sidebarItems"
              :key="item.key"
              type="button"
              class="group flex w-full items-start gap-4 rounded-[18px] px-4 py-4 text-left transition-all duration-300"
              :class="activeTab === item.key
                ? 'border border-[rgba(53,175,146,0.18)] bg-[linear-gradient(135deg,rgba(13,52,43,0.92),rgba(8,24,19,0.92))] shadow-[inset_0_1px_0_rgba(117,255,225,0.08)]'
                : 'border border-transparent hover:border-[rgba(186,139,72,0.14)] hover:bg-[rgba(255,255,255,0.02)]'"
              @click="activeTab = item.key"
            >
              <div
                class="mt-0.5 flex h-11 w-11 items-center justify-center rounded-2xl border transition-colors duration-300"
                :class="activeTab === item.key
                  ? 'border-[rgba(83,214,180,0.28)] bg-[rgba(16,58,48,0.95)] text-[#59d8b7]'
                  : 'border-[rgba(186,139,72,0.16)] bg-[rgba(18,13,10,0.7)] text-[#d3c2a3] group-hover:text-[#f0ddbb]'"
              >
                <component :is="item.icon" :size="20" />
              </div>
              <div class="min-w-0">
                <p class="text-[22px] font-medium tracking-[0.02em]" :class="activeTab === item.key ? 'text-[#f1eadb]' : 'text-[#efe0c5]'">
                  {{ item.title }}
                </p>
                <p class="mt-1 text-sm leading-6 text-[#8d7a5d]">{{ item.subtitle }}</p>
              </div>
            </button>
          </div>

          <div class="quote-card rounded-[20px] border border-[rgba(186,139,72,0.16)] bg-[rgba(10,8,6,0.68)] p-6 backdrop-blur-sm">
            <div class="mb-6 text-[40px] leading-none text-[rgba(205,156,82,0.34)]">"</div>
            <p class="max-w-[160px] text-lg leading-10 text-[#c8ae85]">
              医者，仁术也。<br>
              善治者，先医其心，<br>
              心安则身安。
            </p>
            <div class="mt-8 h-px w-16 bg-[linear-gradient(90deg,rgba(202,152,78,0.55),transparent)]"></div>
            <p class="mt-5 text-sm tracking-[0.16em] text-[#8f7650]">《黄帝内经》</p>
          </div>
        </aside>

        <main class="flex min-w-0 flex-col gap-5">
          <!-- ====== TAB: 对话 (Chat + Avatar) ====== -->
          <template v-if="activeTab === 'chat'">
            <section class="overflow-hidden rounded-[26px] border border-[rgba(196,149,80,0.22)] bg-[rgba(12,9,6,0.54)] shadow-[0_32px_80px_rgba(0,0,0,0.3)] backdrop-blur-sm">
              <div class="grid h-[650px] lg:grid-cols-[58%_42%] 2xl:h-[700px]">
                <div class="relative min-h-[360px] overflow-hidden 2xl:min-h-[500px]">
                  <div
                    class="absolute inset-0 bg-cover bg-center"
                    style="background-image: url('/bencaotujian.png');"
                  ></div>
                  <div class="absolute inset-0 bg-[linear-gradient(90deg,rgba(9,7,5,0.15),rgba(9,7,5,0.1)_44%,rgba(9,7,5,0.55))]"></div>
                  <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(239,207,161,0.08),transparent_38%)]"></div>

                  <div ref="avatarContainerRef" class="absolute inset-0 z-10 avatar-slot"></div>

                  <div v-if="!avatarConnected && !avatarLoading && !avatarPlayBlocked"
                       class="absolute inset-0 z-20 flex cursor-pointer items-center justify-center backdrop-blur-[1px] transition-all duration-500 hover:backdrop-blur-0"
                       @click="startAvatar">
                    <div class="flex flex-col items-center rounded-[24px] border border-[rgba(240,215,171,0.2)] bg-[rgba(5,3,0,0.72)] px-10 py-8 text-center shadow-2xl transition-all duration-300 hover:scale-105 hover:bg-[rgba(10,7,3,0.8)]">
                      <div class="mb-3 flex h-16 w-16 items-center justify-center rounded-full border border-[rgba(74,197,166,0.34)] bg-[rgba(9,33,27,0.78)] text-[#4bd1af]">
                        <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      </div>
                      <p class="text-[22px] tracking-[0.08em] text-[#efe0c4]">点击唤醒通灵</p>
                      <p class="mt-1 text-xs tracking-[0.18em] text-[#8d7a5d]">CLICK TO AWAKEN</p>
                      <p v-if="avatarError" class="mt-3 max-w-[200px] text-xs leading-relaxed text-red-400">{{ avatarError }}</p>
                    </div>
                  </div>

                  <div v-if="avatarLoading"
                       class="absolute inset-0 z-20 flex items-center justify-center bg-[rgba(5,3,0,0.6)] backdrop-blur-sm">
                    <div class="flex flex-col items-center gap-3">
                      <div class="h-10 w-10 animate-spin rounded-full border-2 border-[#4bd1af] border-t-transparent"></div>
                      <p class="text-sm tracking-[0.12em] text-[#c8ae85]">通灵正在降临...</p>
                    </div>
                  </div>

                  <div v-if="avatarPlayBlocked"
                       class="absolute inset-0 z-20 flex items-center justify-center bg-[rgba(5,3,0,0.65)] backdrop-blur-sm">
                    <div class="flex flex-col items-center rounded-[24px] border border-[rgba(240,215,171,0.2)] bg-[rgba(5,3,0,0.72)] px-10 py-8 text-center shadow-2xl"
                         @click="handleResume">
                      <div class="mb-3 flex h-16 w-16 items-center justify-center rounded-full border border-[rgba(255,204,0,0.34)] bg-[rgba(40,35,10,0.78)] text-[#ffcc00]">
                        <svg class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" /></svg>
                      </div>
                      <p class="text-[18px] tracking-[0.08em] text-[#efe0c4]">点击恢复语音</p>
                      <p class="mt-1 text-xs tracking-[0.18em] text-[#8d7a5d]">浏览器限制了自动播放</p>
                    </div>
                  </div>
                </div>

                <div class="relative flex min-h-0 flex-col bg-[linear-gradient(180deg,rgba(14,10,7,0.92),rgba(14,11,8,0.96))] px-7 py-8 md:px-10 md:py-9 2xl:px-12 2xl:py-10">
                  <div class="pointer-events-none absolute inset-y-0 left-0 w-px bg-[linear-gradient(180deg,transparent,rgba(202,151,78,0.28),transparent)]"></div>

                  <div class="flex min-h-0 flex-1 flex-col overflow-hidden rounded-[26px] border border-[rgba(194,147,78,0.14)] bg-[linear-gradient(180deg,rgba(25,18,12,0.9),rgba(15,11,8,0.92))] shadow-[inset_0_1px_0_rgba(255,242,218,0.03)]">
                    <div class="flex items-center justify-between border-b border-[rgba(194,147,78,0.14)] px-5 py-4">
                      <div>
                        <p class="text-sm tracking-[0.2em] text-[#c89f61]">百草通灵</p>
                        <p class="mt-1 text-xs tracking-[0.16em] text-[#7e6848]">HERBAL DIALOGUE</p>
                      </div>
                      <div class="flex items-center gap-2">
                        <span v-if="chatLoading" class="h-2 w-2 animate-pulse rounded-full bg-[#4bd1af]"></span>
                        <div class="rounded-full border border-[rgba(194,147,78,0.14)] bg-[rgba(255,255,255,0.02)] px-3 py-1 text-xs text-[#a98d65]">
                          {{ avatarConnected ? '通灵已连接' : '离线模式' }}
                        </div>
                      </div>
                    </div>

                    <div ref="chatScrollRef" class="custom-scrollbar flex-1 space-y-4 overflow-y-auto px-5 py-5">
                      <div
                        v-for="message in chatMessages"
                        :key="message.id"
                        class="flex"
                        :class="message.role === 'assistant' ? 'justify-start' : 'justify-end'"
                      >
                        <div
                          class="max-w-[88%] rounded-[22px] px-4 py-3"
                          :class="message.role === 'assistant'
                            ? 'rounded-bl-[8px] border border-[rgba(197,150,82,0.16)] bg-[rgba(31,23,15,0.95)] text-[#dbc39f]'
                            : 'rounded-br-[8px] border border-[rgba(74,197,166,0.18)] bg-[linear-gradient(135deg,rgba(10,52,43,0.96),rgba(7,27,23,0.96))] text-[#e7f8f2]'"
                        >
                          <div class="mb-2 flex items-center gap-2 text-[11px] tracking-[0.18em]">
                            <span :class="message.role === 'assistant' ? 'text-[#c7a36a]' : 'text-[#62dfbc]'">
                              {{ message.role === 'assistant' ? '通灵助手' : '你' }}
                            </span>
                            <span class="text-[#6f5d44]">{{ message.time }}</span>
                          </div>
                          <p class="text-[15px] leading-8 whitespace-pre-wrap">{{ message.content }}</p>
                        </div>
                      </div>
                      <div v-if="chatLoading" class="flex justify-start">
                        <div class="rounded-[22px] rounded-bl-[8px] border border-[rgba(197,150,82,0.16)] bg-[rgba(31,23,15,0.95)] px-4 py-3 text-[#dbc39f]">
                          <div class="flex items-center gap-1.5">
                            <span class="h-2 w-2 animate-bounce rounded-full bg-[#c7a36a]" style="animation-delay:0ms"></span>
                            <span class="h-2 w-2 animate-bounce rounded-full bg-[#c7a36a]" style="animation-delay:150ms"></span>
                            <span class="h-2 w-2 animate-bounce rounded-full bg-[#c7a36a]" style="animation-delay:300ms"></span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="border-t border-[rgba(194,147,78,0.14)] px-5 pb-5 pt-4">
                      <div class="mb-4 flex flex-wrap gap-2">
                        <button
                          v-for="prompt in quickPrompts"
                          :key="prompt"
                          type="button"
                          class="rounded-full border border-[rgba(194,147,78,0.14)] bg-[rgba(255,255,255,0.02)] px-3 py-1.5 text-xs text-[#bfa47a] transition-all duration-300 hover:border-[rgba(78,203,170,0.22)] hover:text-[#e7d3b0]"
                          @click="handleQuickPrompt(prompt)"
                        >
                          {{ prompt }}
                        </button>
                      </div>

                      <div class="flex items-center gap-3 rounded-[18px] border border-[rgba(194,147,78,0.16)] bg-[rgba(11,8,6,0.86)] px-4 py-3">
                        <div class="flex h-10 w-10 items-center justify-center rounded-full border border-[rgba(74,197,166,0.18)] bg-[rgba(9,33,27,0.78)] text-[#4bd1af]">
                          <MessageCircleMore :size="18" />
                        </div>
                        <input ref="chatInputRef" v-model="chatInput"
                          type="text"
                          placeholder="请输入你想了解的问题..."
                          class="min-w-0 flex-1 bg-transparent text-sm text-[#d9c09a] placeholder-[#766247] outline-none"
                          @keydown.enter="handleSend"
                        />
                        <button
                          type="button"
                          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-[rgba(74,197,166,0.22)] bg-[linear-gradient(135deg,rgba(12,72,58,0.92),rgba(7,35,28,0.92))] text-[#63dfbf] transition-transform duration-300 hover:scale-105 disabled:opacity-40"
                          :disabled="!chatInput.trim() || chatLoading"
                          @click="handleSend"
                        >
                          <SendHorizonal :size="18" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <section class="rounded-[22px] border border-[rgba(196,149,80,0.14)] bg-[rgba(10,8,6,0.56)] px-5 py-5 md:px-6 md:py-6 2xl:px-8">
              <div class="mb-4 flex items-center gap-3">
                <h2 class="text-[34px] font-medium tracking-[0.08em] text-[#f1ddb8]">相关本草</h2>
                <span class="h-px flex-1 bg-[linear-gradient(90deg,rgba(202,151,78,0.5),transparent)]"></span>
              </div>
              <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
                <article
                  v-for="herb in relatedHerbs"
                  :key="herb.name"
                  class="group flex items-center gap-4 rounded-[18px] border border-[rgba(196,149,80,0.14)] bg-[linear-gradient(180deg,rgba(28,20,13,0.88),rgba(16,12,8,0.9))] px-4 py-4 transition-all duration-300 hover:-translate-y-0.5 hover:border-[rgba(204,161,95,0.26)] cursor-pointer"
                  @click="activeTab = 'atlas'"
                >
                  <div class="flex h-16 w-16 shrink-0 items-center justify-center rounded-[16px] border border-[rgba(196,149,80,0.12)] bg-[radial-gradient(circle,rgba(82,58,29,0.32),transparent_70%)]">
                    <img :src="herb.image" :alt="herb.name" class="h-12 w-12 object-contain transition-transform duration-300 group-hover:scale-110" />
                  </div>
                  <div class="min-w-0">
                    <p class="text-[26px] leading-none tracking-[0.06em] text-[#f0dcb8]">{{ herb.name }}</p>
                    <p class="mt-2 text-sm text-[#947b57]">{{ herb.tagline }}</p>
                  </div>
                </article>
              </div>
            </section>
          </template>

          <!-- ====== TAB: 本草图鉴 ====== -->
          <template v-if="activeTab === 'atlas'">
            <section class="overflow-hidden rounded-[26px] border border-[rgba(196,149,80,0.22)] bg-[rgba(12,9,6,0.54)] shadow-[0_32px_80px_rgba(0,0,0,0.3)] backdrop-blur-sm p-6 md:p-8">
              <div class="flex items-center gap-3 mb-6">
                <span class="h-px w-10 bg-[linear-gradient(90deg,rgba(205,155,81,0.8),transparent)]"></span>
                <h2 class="text-[34px] font-medium tracking-[0.08em] text-[#f1ddb8]">本草图鉴</h2>
                <span class="h-px flex-1 bg-[linear-gradient(90deg,rgba(202,151,78,0.5),transparent)]"></span>
              </div>
              <HerbGuide />
            </section>
          </template>

          <!-- ====== TAB: 节气 ====== -->
          <template v-if="activeTab === 'solar'">
            <section class="overflow-hidden rounded-[26px] border border-[rgba(196,149,80,0.22)] bg-[rgba(12,9,6,0.54)] shadow-[0_32px_80px_rgba(0,0,0,0.3)] backdrop-blur-sm p-6 md:p-8">
              <div class="flex items-center gap-3 mb-6">
                <span class="h-px w-10 bg-[linear-gradient(90deg,rgba(205,155,81,0.8),transparent)]"></span>
                <h2 class="text-[34px] font-medium tracking-[0.08em] text-[#f1ddb8]">二十四节气</h2>
                <span class="h-px flex-1 bg-[linear-gradient(90deg,rgba(202,151,78,0.5),transparent)]"></span>
              </div>
              <SolarTermWheel />
            </section>
          </template>

          <!-- ====== TAB: 养生知识 ====== -->
          <template v-if="activeTab === 'wellness'">
            <section class="overflow-hidden rounded-[26px] border border-[rgba(196,149,80,0.22)] bg-[rgba(12,9,6,0.54)] shadow-[0_32px_80px_rgba(0,0,0,0.3)] backdrop-blur-sm p-6 md:p-8">
              <div class="flex items-center gap-3 mb-6">
                <span class="h-px w-10 bg-[linear-gradient(90deg,rgba(205,155,81,0.8),transparent)]"></span>
                <h2 class="text-[34px] font-medium tracking-[0.08em] text-[#f1ddb8]">养生知识</h2>
                <span class="h-px flex-1 bg-[linear-gradient(90deg,rgba(202,151,78,0.5),transparent)]"></span>
              </div>

              <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                <div v-for="item in wellnessItems" :key="item.title"
                     class="group rounded-[20px] border border-[rgba(196,149,80,0.14)] bg-[linear-gradient(180deg,rgba(28,20,13,0.88),rgba(16,12,8,0.9))] p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-[rgba(204,161,95,0.26)]">
                  <div class="flex items-center gap-3 mb-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-xl border border-[rgba(196,149,80,0.12)] bg-[radial-gradient(circle,rgba(82,58,29,0.32),transparent_70%)] text-xl">
                      {{ item.icon }}
                    </div>
                    <h3 class="text-lg font-medium text-[#f0dcb8] tracking-[0.04em]">{{ item.title }}</h3>
                  </div>
                  <p class="text-sm text-[#947b57] leading-7">{{ item.desc }}</p>
                  <div class="mt-3 flex flex-wrap gap-2">
                    <span v-for="tag in item.tags" :key="tag"
                          class="rounded-full border border-[rgba(74,197,166,0.18)] bg-[rgba(9,33,27,0.5)] px-2.5 py-0.5 text-[11px] text-[#4bd1af]">
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </div>
            </section>
          </template>
        </main>
      </div>
    </div>

    <!-- Herb Detail Modal -->
    <Teleport to="body">
      <transition name="modal-enter">
        <div v-if="detailHerb" class="fixed inset-0 z-[100] flex items-center justify-center p-4"
             @click.self="detailHerb = null">
          <div class="absolute inset-0 bg-black/70 backdrop-blur-sm"></div>
          <div class="relative w-[520px] max-h-[85vh] overflow-y-auto rounded-2xl border border-[rgba(196,149,80,0.3)] bg-gradient-to-b from-[#1a1208] to-[#0e0a05] p-6 shadow-2xl custom-scrollbar">
            <div class="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-[rgba(202,151,78,0.3)] to-transparent"></div>
            <div class="flex justify-between items-start mb-6">
              <div class="flex items-center gap-4">
                <div class="w-20 h-20 rounded-xl bg-gradient-to-b from-black/40 to-black/20 border border-[rgba(196,149,80,0.14)] overflow-hidden flex items-center justify-center p-2">
                  <img :src="detailHerb.image" :alt="detailHerb.name" class="w-full h-full object-contain" />
                </div>
                <div>
                  <h3 class="text-xl font-bold text-[#f0dcb8] font-serif">{{ detailHerb.name }}</h3>
                  <p class="text-xs text-[#8d7a5d] italic mt-0.5">{{ detailHerb.latin }}</p>
                  <span class="inline-block mt-1 text-[10px] px-2 py-0.5 rounded-full bg-[rgba(9,33,27,0.5)] text-[#4bd1af] border border-[rgba(74,197,166,0.18)]">
                    {{ detailHerb.category }}
                  </span>
                </div>
              </div>
              <button @click="detailHerb = null"
                      class="w-8 h-8 rounded-lg flex items-center justify-center text-[#8d7a5d] hover:text-[#f0dcb8] hover:bg-[rgba(255,255,255,0.05)] transition-all">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div class="flex flex-wrap gap-2 mb-5">
              <span class="px-3 py-1 rounded-lg border border-[rgba(196,149,80,0.14)] text-xs text-[#dbc39f] bg-[rgba(31,23,15,0.6)]">{{ detailHerb.nature }}</span>
              <span v-for="f in detailHerb.flavors" :key="f"
                    class="px-3 py-1 rounded-lg border border-[rgba(196,149,80,0.14)] text-xs text-[#dbc39f] bg-[rgba(31,23,15,0.6)]">{{ f }}</span>
              <span v-for="m in detailHerb.meridians" :key="m"
                    class="px-3 py-1 rounded-full text-[10px] bg-[rgba(9,33,27,0.5)] text-[#4bd1af] border border-[rgba(74,197,166,0.18)]">
                归{{ m }}
              </span>
            </div>
            <div class="space-y-3 text-sm">
              <div class="p-4 rounded-xl border border-[rgba(196,149,80,0.14)] bg-[rgba(31,23,15,0.6)]">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-[10px] text-[#4bd1af] uppercase tracking-wider font-medium">功效</span>
                  <span class="flex-1 h-px bg-gradient-to-r from-[rgba(74,197,166,0.2)] to-transparent"></span>
                </div>
                <p class="text-[#dbc39f] leading-relaxed">{{ detailHerb.efficacy }}</p>
              </div>
              <div class="p-4 rounded-xl border border-[rgba(196,149,80,0.14)] bg-[rgba(31,23,15,0.6)]">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-[10px] text-[#c89f61] uppercase tracking-wider font-medium">用法用量</span>
                  <span class="flex-1 h-px bg-gradient-to-r from-[rgba(202,151,78,0.2)] to-transparent"></span>
                </div>
                <p class="text-[#bba27d] leading-relaxed">{{ detailHerb.usage }}</p>
              </div>
              <div class="p-4 rounded-xl border border-[rgba(255,204,0,0.14)] bg-gradient-to-br from-[rgba(255,204,0,0.03)] to-transparent">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-[10px] text-[#ffcc00] uppercase tracking-wider font-medium">⚠ 注意事项</span>
                  <span class="flex-1 h-px bg-gradient-to-r from-[rgba(255,204,0,0.2)] to-transparent"></span>
                </div>
                <p class="text-[#e6cfaa] leading-relaxed">{{ detailHerb.caution }}</p>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import {
  Heart,
  Leaf,
  MessageCircleMore,
  SendHorizonal,
  Sun,
} from 'lucide-vue-next'
import { useAvatarSDK } from '@/composables/useAvatarSDK'
import { sendChatMessage } from '@/api'
import SolarTermWheel from '@/modules/herbsage/SolarTermWheel.vue'
import HerbGuide from '@/modules/herbsage/HerbGuide.vue'

const chatMessages = ref([
  {
    id: 'welcome',
    role: 'assistant',
    time: (() => { const n = new Date(); return `${String(n.getHours()).padStart(2,'0')}:${String(n.getMinutes()).padStart(2,'0')}` })(),
    content: '年轻人，你来了。本灵在此等候多时。\n有什么关于本草种植、节气养生的问题，尽管问吧。',
  },
])
const chatScrollRef = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (chatScrollRef.value) {
    chatScrollRef.value.scrollTop = chatScrollRef.value.scrollHeight
  }
}

const formatTime = () => {
  const now = new Date()
  return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
}

let avatarSpeaking = false

const {
  isConnected: avatarConnected,
  isLoading: avatarLoading,
  playNotAllowed: avatarPlayBlocked,
  error: avatarError,
  initAndStart,
  sendText,
  interrupt,
  resume: handleResume,
} = useAvatarSDK({
  onSubtitle: () => {
    avatarSpeaking = true
  },
  onNlpResponse: () => {
    avatarSpeaking = true
  },
})

const activeTab = ref('chat')
const avatarContainerRef = ref(null)

const startAvatar = async () => {
  if (!avatarContainerRef.value) return
  await initAndStart(avatarContainerRef.value)
}

const sidebarItems = [
  { key: 'chat', title: '百草通灵', subtitle: '与通灵对话', icon: MessageCircleMore },
  { key: 'solar', title: '二十四节气', subtitle: '节气养生指南', icon: Sun },
  { key: 'atlas', title: '本草图鉴', subtitle: '药材详解与知识', icon: Leaf },
  { key: 'wellness', title: '养生知识', subtitle: '养生方法与调理', icon: Heart },
]

const chatInput = ref('')
const chatInputRef = ref(null)
const chatLoading = ref(false)

const handleSend = async () => {
  const text = chatInput.value.trim()
  if (!text || chatLoading.value) return
  chatInput.value = ''

  chatMessages.value.push({
    id: 'msg_' + Date.now(),
    role: 'user',
    time: formatTime(),
    content: text,
  })
  await scrollToBottom()

  chatLoading.value = true

  try {
    const res = await sendChatMessage(text, true)
    let reply = ''
    if (res && res.data && res.data.content) {
      reply = res.data.content
    } else {
      reply = '本灵暂时无法回应，请稍后再试。'
    }

    chatMessages.value.push({
      id: 'reply_' + Date.now(),
      role: 'assistant',
      time: formatTime(),
      content: reply,
    })
    await scrollToBottom()

    if (avatarConnected.value && reply) {
      try {
        avatarSpeaking = false
        await sendText(reply, { nlp: false, interactive_mode: 0 })
      } catch (e) {
        console.error('[AvatarSDK] sendText failed:', e)
      }
    }
  } catch (e) {
    const fallbackReplies = [
      '嗯…你问得好。按《本草纲目》所载，此法可行。',
      '俗话说"春生夏长，秋收冬藏"，此时节宜养肝护肝。',
      '此物性味甘温，入脾肺经，乃补气之良药。',
      '本灵观之，此事颇有讲究。待我慢慢道来~',
      '且听本灵一言：养生之道，贵在坚持。',
    ]
    const reply = fallbackReplies[Math.floor(Math.random() * fallbackReplies.length)]
    await new Promise((r) => setTimeout(r, 800 + Math.random() * 800))
    chatMessages.value.push({
      id: 'reply_' + Date.now(),
      role: 'assistant',
      time: formatTime(),
      content: reply,
    })
    await scrollToBottom()

    if (avatarConnected.value) {
      try {
        avatarSpeaking = false
        await sendText(reply, { nlp: false, interactive_mode: 0 })
      } catch (e2) {
        console.error('[AvatarSDK] sendText failed:', e2)
      }
    }
  } finally {
    chatLoading.value = false
    await scrollToBottom()
  }
}

const handleQuickPrompt = (prompt) => {
  chatInput.value = prompt
  handleSend()
}

const quickPrompts = [
  '人参与黄芪有什么区别？',
  '当前棚内环境如何？',
  '今日养生建议',
  '如何预防根腐病？',
  '讲讲黄芪的功效',
  '推荐时令药膳',
]

const relatedHerbs = [
  { name: '黄芪', tagline: '补气固表', image: '/herb-astragalus.png' },
  { name: '灵芝', tagline: '益气安神', image: '/herb-lingzhi.png' },
  { name: '石斛', tagline: '滋阴生津', image: '/herb-dendrobium.png' },
  { name: '枸杞子', tagline: '滋补肝肾', image: '/herb-goji.png' },
  { name: '三七', tagline: '补血活血', image: '/herb-notoginseng.png' },
]

const detailHerb = ref(null)

const wellnessItems = [
  {
    icon: '🫖',
    title: '药膳养生',
    desc: '根据四时节气，选用当季药材搭配食材，以食为药、以膳为养，达到调理身体、预防疾病的目的。',
    tags: ['四季药膳', '体质调理', '食疗方'],
  },
  {
    icon: '🧘',
    title: '五禽戏',
    desc: '华佗创编的导引养生功法，模仿虎、鹿、熊、猿、鸟五种动物的动作，舒筋活络、调和气血。',
    tags: ['导引术', '强身健体', '气血调和'],
  },
  {
    icon: '🌿',
    title: '节气养生',
    desc: '顺应二十四节气变化，调整起居饮食。春养肝、夏养心、秋养肺、冬养肾，天人合一。',
    tags: ['顺时养生', '四季调养', '天人合一'],
  },
  {
    icon: '💊',
    title: '膏方进补',
    desc: '冬季膏方进补是中医传统养生方法，根据个人体质辨证施补，滋补强身、延年益寿。',
    tags: ['冬令进补', '辨证施补', '滋补强身'],
  },
  {
    icon: '🍵',
    title: '本草茶饮',
    desc: '以中药材代茶饮用，简便易行。菊花清肝明目、枸杞滋补肝肾、黄芪补气固表。',
    tags: ['代茶饮', '简便养生', '日常保健'],
  },
  {
    icon: '🪷',
    title: '经络穴位',
    desc: '通过按摩特定穴位疏通经络、调理脏腑。足三里健脾胃、合谷穴止痛、太冲穴疏肝理气。',
    tags: ['穴位按摩', '经络疏通', '自我保健'],
  },
]
</script>

<style scoped>
.quote-card {
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.02);
}

.avatar-slot {
  width: 100% !important;
  height: 100% !important;
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  transform: translateY(-15%) !important;
}
.avatar-slot video,
.avatar-slot canvas,
.avatar-slot img {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;
  transform: translateY(-15%) !important;
}

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
