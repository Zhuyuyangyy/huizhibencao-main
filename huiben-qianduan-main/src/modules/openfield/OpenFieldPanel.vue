<template>
  <div class="flex-1 flex flex-col min-h-0" style="height: 100%;">
    <div class="flex-1 flex gap-4 min-h-0">

      <!-- ========== LEFT COLUMN ========== -->
      <div class="w-[28%] flex flex-col gap-4 overflow-y-auto custom-scrollbar pr-1">

        <!-- 环境监测 -->
        <div class="tech-panel flex flex-col p-4 pt-3">
          <div class="tech-panel-inner"></div>
          <div class="panel-title">
            <Leaf :size="16" class="text-green-400 mr-2" /> 环境监测
            <div class="panel-title-line"></div>
          </div>

          <div class="flex justify-between items-end mb-2">
            <div class="flex items-center gap-1 text-xs text-[var(--color-cyan-glow)]">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              气象雷达
            </div>
            <div class="text-xs text-gray-400">亳州市 谯城区</div>
          </div>

          <div class="flex gap-4 mb-4">
            <div class="w-1/3 flex flex-col justify-center">
              <div class="text-3xl font-bold text-white num-font mb-2">25<span class="text-base text-gray-400">°C</span></div>
              <div class="text-xs text-gray-400 space-y-1">
                <p>东南风 2级</p>
                <p>湿度 <span class="text-[var(--color-cyan-glow)]">65%</span></p>
                <p>降水概率 20%</p>
              </div>
            </div>
            <div class="w-2/3 h-[120px] bg-[#051822] border border-[#133c46] rounded relative overflow-hidden flex items-center justify-center">
              <div class="absolute inset-0 bg-[url('/leidaditu.png')] bg-cover bg-center"></div>
              <div class="radar-scan"></div>
              <div class="absolute w-20 h-20 bg-gradient-to-tr from-green-500 via-yellow-400 to-red-500 rounded-full blur-xl opacity-60"></div>
              <div class="absolute w-12 h-12 bg-red-500 rounded-full blur-lg opacity-80"></div>
            </div>
          </div>

          <div class="flex items-center gap-1 text-[10px] text-gray-500 mb-4">
            <span>0</span>
            <div class="h-1 flex-1 flex rounded overflow-hidden">
              <div class="w-1/6 bg-blue-500"></div><div class="w-1/6 bg-cyan-400"></div>
              <div class="w-1/6 bg-green-500"></div><div class="w-1/6 bg-yellow-400"></div>
              <div class="w-1/6 bg-orange-500"></div><div class="w-1/6 bg-red-500"></div>
            </div>
            <span>100</span>
          </div>

          <div class="flex justify-between">
            <div class="text-center">
              <p class="text-xs text-gray-400 mb-1">今天</p>
              <p class="text-sm text-[var(--color-cyan-glow)] num-font">18~26°C</p>
              <svg class="w-5 h-5 text-gray-300 mx-auto my-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 15a4 4 0 004 4h9a5 5 0 10-4.5-7.2A3.5 3.5 0 003 15z" />
              </svg>
              <p class="text-xs text-gray-400">多云</p>
            </div>
            <div class="text-center">
              <p class="text-xs text-gray-400 mb-1">明天</p>
              <p class="text-sm text-white num-font">20~28°C</p>
              <svg class="w-5 h-5 text-gray-300 mx-auto my-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 3v1m0 16v1m8.66-14.66l-.71.71M4.05 19.95l-.71.71M21 12h-1M4 12H3m15.66 7.66l-.71-.71M4.05 4.05l-.71-.71" />
              </svg>
              <p class="text-xs text-gray-400">多云转晴</p>
            </div>
            <div class="text-center">
              <p class="text-xs text-gray-400 mb-1">后天</p>
              <p class="text-sm text-white num-font">21~30°C</p>
              <svg class="w-5 h-5 text-yellow-400 mx-auto my-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <circle cx="12" cy="12" r="5" stroke-width="1.5" /><path stroke-linecap="round" stroke-width="1.5" d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
              </svg>
              <p class="text-xs text-gray-400">晴转多云</p>
            </div>
          </div>
        </div>

        <!-- 土壤墒情监测 -->
        <div class="tech-panel flex flex-col p-4 pt-3">
          <div class="tech-panel-inner"></div>
          <div class="panel-title">
            <svg class="w-4 h-4 text-green-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            土壤墒情监测
            <div class="panel-title-line"></div>
          </div>

          <div class="flex border-b border-[#133c46] mb-2 text-xs">
            <div class="px-4 py-1 text-[var(--color-cyan-glow)] border-b-2 border-[var(--color-cyan-glow)] cursor-pointer">10cm层</div>
            <div class="px-4 py-1 text-gray-400 hover:text-white cursor-pointer">20cm层</div>
            <div class="px-4 py-1 text-gray-400 hover:text-white cursor-pointer">40cm层</div>
            <div class="px-4 py-1 text-gray-400 hover:text-white cursor-pointer">60cm层</div>
          </div>

          <div class="text-xs text-gray-400 self-end mb-1">土壤湿度 (%)</div>
          <div ref="moistureChartRef" class="w-full" style="height: 140px;"></div>
        </div>

        <!-- 土壤养分检测 -->
        <div class="tech-panel flex flex-col p-4 pt-3">
          <div class="tech-panel-inner"></div>
          <div class="panel-title">
            <svg class="w-4 h-4 text-green-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            土壤养分检测 <span class="text-xs text-gray-500 ml-2">(mg/kg)</span>
            <div class="panel-title-line"></div>
          </div>

          <div class="flex items-center gap-4">
            <div class="w-[110px] h-[110px] relative flex-shrink-0">
              <svg viewBox="0 0 100 100" class="w-full h-full -rotate-90">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#0a2a36" stroke-width="8" />
                <circle cx="50" cy="50" r="40" fill="none" stroke="var(--color-cyan-glow)" stroke-width="8" stroke-dasharray="180 251" />
                <circle cx="50" cy="50" r="30" fill="none" stroke="#008877" stroke-width="2" stroke-dasharray="4 4" />
                <circle cx="50" cy="50" r="48" fill="none" stroke="#005566" stroke-width="1" stroke-dasharray="10 10" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center text-[var(--color-cyan-glow)]">
                <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
            </div>
            <div class="flex-1 space-y-2">
              <div v-for="nutrient in nutrients" :key="nutrient.name" class="flex items-center justify-between text-sm">
                <span class="flex items-center gap-2">
                  <div class="w-1.5 h-1.5 rounded-full" :style="{ backgroundColor: nutrient.color }"></div>
                  {{ nutrient.name }}
                </span>
                <span class="num-font text-white font-bold">{{ nutrient.value }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========== CENTER COLUMN ========== -->
      <div class="w-[44%] flex flex-col relative">

        <!-- Top Stats Row -->
        <div class="flex gap-2 mb-3 h-[65px] shrink-0">
          <div v-for="(card, idx) in topStats" :key="idx"
               class="flex-1 flex items-center p-2 rounded border-l-2"
               :class="card.warning ? 'border-l-[var(--color-alert-warning)] bg-gradient-to-r from-[var(--color-alert-warning)]/5 to-transparent' : 'border-l-[var(--color-cyan-glow)] bg-gradient-to-r from-[var(--color-cyan-dim)] to-transparent'">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm"
                   :class="card.warning ? 'bg-[#332200] text-[var(--color-alert-warning)]' : 'bg-[#003333] text-[var(--color-cyan-glow)]'">
                {{ card.icon }}
              </div>
              <div>
                <div class="text-[10px] text-gray-400">{{ card.label }}</div>
                <div class="text-sm font-bold num-font" :class="card.warning ? 'text-[var(--color-alert-warning)]' : 'text-white'">
                  {{ card.value }}
                  <span v-if="card.trend" class="text-[10px] text-green-400 ml-1">↑ 12%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Central Map / Video Area -->
        <div class="flex-1 relative rounded-lg overflow-hidden border border-[#133c46] bg-[#020a10]">
          <video class="w-full h-full object-cover" autoplay loop muted playsinline>
            <source src="/wupeng.mp4" type="video/mp4">
          </video>

          <!-- Overlay glow -->
          <div class="absolute inset-0 pointer-events-none"
               style="background: linear-gradient(135deg, rgba(0,255,204,0.05) 0%, transparent 50%, rgba(0,255,204,0.02) 100%);"></div>

          <!-- Corner info -->
          <div class="absolute top-3 left-3 z-10">
            <div class="bg-black/60 backdrop-blur-sm px-2.5 py-1 rounded text-xs text-[var(--color-cyan-glow)] border border-[var(--color-border)]">
              A3 区块 · 多光谱巡检
            </div>
          </div>
          <div class="absolute top-3 right-3 z-10">
            <div class="bg-black/60 backdrop-blur-sm px-2.5 py-1 rounded text-xs text-gray-300 num-font border border-[#133c46]">
              {{ currentTime }}
            </div>
          </div>

          <!-- Drone HUD overlay -->
          <div class="absolute bottom-4 left-4 z-10 flex gap-1 text-[10px] text-gray-400">
            <div class="bg-black/60 px-2 py-1 rounded">ALT 85m</div>
            <div class="bg-black/60 px-2 py-1 rounded">SPD 8m/s</div>
            <div class="bg-black/60 px-2 py-1 rounded">HDG 180°</div>
          </div>
        </div>

        <!-- Bottom Controls -->
        <div class="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-1 z-20">
          <button v-for="(btn, idx) in bottomControls" :key="idx"
                  class="flex flex-col items-center justify-center px-4 h-14 text-xs transition-all duration-300 cursor-pointer"
                  :class="idx === 0
                    ? 'bg-[var(--color-cyan-dim)] border border-[var(--color-border-strong)] text-[var(--color-cyan-glow)] rounded-l'
                    : idx === bottomControls.length - 1
                      ? 'bg-[rgba(0,50,60,0.5)] border border-[#1a5051] text-[var(--color-text-secondary)] hover:bg-[var(--color-cyan-dim)] rounded-r'
                      : 'bg-[rgba(0,50,60,0.5)] border border-[#1a5051] text-[var(--color-text-secondary)] hover:bg-[var(--color-cyan-dim)]'"
          >
            <span class="text-lg mb-0.5">{{ btn.icon }}</span>
            <span>{{ btn.label }}</span>
          </button>
        </div>

        <!-- Bottom glow -->
        <div class="absolute bottom-8 left-1/2 -translate-x-1/2 w-36 h-36 bg-[var(--color-cyan-glow)] opacity-[0.06] blur-3xl rounded-full pointer-events-none"></div>
      </div>

      <!-- ========== RIGHT COLUMN ========== -->
      <div class="w-[28%] flex flex-col gap-4 overflow-y-auto custom-scrollbar pr-1">

        <!-- 视听融合 -->
        <div class="tech-panel flex flex-col p-4 pt-3">
          <div class="tech-panel-inner"></div>
          <div class="panel-title">
            <svg class="w-4 h-4 text-green-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
            视听融合 · AI病虫害预警
            <div class="panel-title-line"></div>
          </div>

          <div class="flex justify-between items-center text-xs text-gray-400 mb-2">
            <span class="flex items-center gap-1">
              <svg class="w-3 h-3 text-[var(--color-cyan-glow)]" fill="currentColor" viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
              声学梅尔频谱
            </span>
            <span>设备: acoustic-12#</span>
          </div>

          <div class="relative border border-[#133c46] rounded overflow-hidden" style="height: 150px;">
            <div class="absolute inset-0 spectrogram-bg opacity-70"></div>
            <div class="absolute inset-0" style="background-image: linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px); background-size: 20% 20%;"></div>
            <div class="absolute left-1 top-0 bottom-6 flex flex-col justify-between text-[9px] text-gray-500 py-1">
              <span>8k</span><span>4k</span><span>2k</span><span>1k</span><span>500</span><span>0</span>
            </div>
            <div class="absolute left-6 right-2 bottom-0 flex justify-between text-[9px] text-gray-500 pb-1">
              <span>00:00</span><span>06:00</span><span>12:00</span><span>18:00</span><span>24:00</span>
            </div>
            <div class="absolute top-0 bottom-5 right-[10%] w-[30%] bg-[rgba(255,51,102,0.15)] border-x border-[#ff3366] flex flex-col items-center justify-start pt-4 z-10">
              <div class="bg-[rgba(255,51,102,0.8)] text-white text-[10px] px-2 py-1 rounded flex items-center gap-1 shadow-[0_0_10px_#ff3366]">
                <AlertTriangle :size="12" /> 检测到害虫活动！
              </div>
            </div>
            <svg class="absolute inset-0 w-full h-[calc(100%-20px)] z-0" preserveAspectRatio="none" viewBox="0 0 100 100">
              <path d="M0,50 L5,45 L10,55 L15,48 L20,52 L25,30 L30,60 L35,40 L40,50 L45,48 L50,55 L55,40 L60,80 L65,20 L70,90 L75,10 L80,60 L85,45 L90,55 L95,48 L100,50" fill="none" stroke="var(--color-cyan-glow)" stroke-width="0.5" filter="drop-shadow(0 0 2px var(--color-cyan-glow))"></path>
            </svg>
          </div>
        </div>

        <!-- AI识别结果 -->
        <div class="tech-panel flex flex-col p-4 pt-3">
          <div class="tech-panel-inner"></div>
          <div class="panel-title mb-2">
            <svg class="w-3 h-3 text-[var(--color-cyan-glow)] mr-1" fill="currentColor" viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
            AI识别结果
          </div>

          <div class="border border-[rgba(255,51,102,0.5)] bg-[rgba(255,51,102,0.1)] p-3 rounded-r-md relative">
            <div class="absolute left-0 top-0 w-[3px] h-full bg-[var(--color-alert-danger)] shadow-[0_0_8px_var(--color-alert-danger)]"></div>
            <div class="flex gap-3">
              <div class="flex-1">
                <div class="flex items-start gap-2 mb-2">
                  <AlertTriangle :size="18" class="text-[var(--color-alert-danger)] shrink-0 mt-0.5" />
                  <div>
                    <h3 class="text-[var(--color-alert-danger)] font-bold text-base leading-tight">草地贪夜蛾</h3>
                    <p class="text-xs text-gray-400 italic">Spodoptera frugiperda</p>
                  </div>
                </div>
                <div class="space-y-1 mt-2">
                  <p class="text-xs text-gray-300">置信度: <span class="text-[var(--color-alert-danger)] font-bold num-font">92.6%</span></p>
                  <p class="text-xs text-gray-300">发生概率: <span class="text-[var(--color-alert-danger)] font-bold">高</span></p>
                </div>
              </div>
              <div class="w-[80px] h-[80px] border border-[rgba(255,51,102,0.5)] rounded overflow-hidden relative shrink-0">
                <img src="/chongzi.png" alt="Pest" class="w-full h-full object-cover">
                <div class="absolute top-0 left-0 w-full h-[2px] bg-[var(--color-alert-danger)] shadow-[0_0_8px_var(--color-alert-danger)] animate-scan-line"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI决策建议 -->
        <div class="tech-panel flex flex-col p-4 pt-3">
          <div class="tech-panel-inner"></div>
          <div class="panel-title mb-2">
            <svg class="w-4 h-4 text-[#00d0ff] mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            AI决策建议
          </div>

          <div class="border border-[rgba(0,208,255,0.3)] bg-[rgba(0,208,255,0.05)] p-3 rounded relative overflow-hidden">
            <div class="space-y-1.5 z-10 relative">
              <p class="text-[#00d0ff] font-bold text-sm mb-2">建议使用生物农药进行防治</p>
              <p class="text-xs text-gray-300 flex items-center gap-2"><span class="text-gray-500 w-16 shrink-0">推荐药剂:</span> Bt可湿性粉剂</p>
              <p class="text-xs text-gray-300 flex items-center gap-2"><span class="text-gray-500 w-16 shrink-0">推荐浓度:</span> 800-1000倍液</p>
              <p class="text-xs text-gray-300 flex items-center gap-2"><span class="text-gray-500 w-16 shrink-0">最佳时间:</span> 傍晚施药</p>
            </div>
            <svg class="absolute right-[-10px] top-1/2 -translate-y-1/2 w-16 h-16 text-[#00d0ff] opacity-20" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2a2 2 0 012 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 017 7h1a1 1 0 011 1v3a1 1 0 01-1 1h-1.27A7.02 7.02 0 0114 22h-4a7.02 7.02 0 01-6.73-4H2a1 1 0 01-1-1v-3a1 1 0 011-1h1a7 7 0 017-7h1v-1.27c-.6-.34-1-.99-1-1.73a2 2 0 012-2z"/>
            </svg>
          </div>
        </div>

        <!-- 多光谱无人机监测 -->
        <div class="tech-panel flex flex-col p-4 pt-3">
          <div class="tech-panel-inner"></div>
          <div class="panel-title">
            <svg class="w-3 h-3 text-green-400 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
            多光谱无人机监测
            <div class="panel-title-line"></div>
          </div>

          <div class="flex justify-between border-b border-[#133c46] mb-2 text-xs pb-1">
            <div class="px-2 text-[var(--color-cyan-glow)] border-b-2 border-[var(--color-cyan-glow)] cursor-pointer">可见光</div>
            <div class="px-2 text-gray-400 hover:text-white cursor-pointer">NDVI</div>
            <div class="px-2 text-gray-400 hover:text-white cursor-pointer">红边</div>
            <div class="px-2 text-gray-400 hover:text-white cursor-pointer">热成像</div>
          </div>

          <div class="relative border border-[#133c46] rounded overflow-hidden group" style="height: 130px;">
            <img src="/wurenji.png" alt="Drone View" class="w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500">
            <div class="absolute inset-0 opacity-30"
                 style="background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCI+PHBhdGggZD0iTTAgMGg0MHY0MEgweiIgZmlsbD0ibm9uZSIvPjxwYXRoIGQ9Ik0wIDM5LjVoNDBWMDBWMHoiIGZpbGw9InJnYmEoMCwyNTUsMjA0LDAuMikiLz48L3N2Zz4='); background-size: 40px 40px;">
            </div>
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 border border-[var(--color-cyan-glow)] opacity-50 flex items-center justify-center">
              <div class="w-1 h-1 bg-[var(--color-cyan-glow)]"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Status Bar -->
    <div class="h-[30px] flex justify-between items-center px-4 text-[11px] text-gray-400 shrink-0 border-t border-[#133c46] bg-[rgba(3,11,20,0.8)] mt-3">
      <div class="flex gap-4">
        <span>设备在线率 <span class="text-[var(--color-cyan-glow)] num-font">98.6%</span></span>
        <span>数据更新时间 <span class="num-font text-gray-300">{{ currentTime }}</span></span>
        <span>设备总数 <span class="num-font text-white">256</span></span>
        <span>在线设备 <span class="text-[var(--color-cyan-glow)] num-font">252</span></span>
      </div>
      <div class="flex items-center gap-4">
        <span>告警统计</span>
        <div class="flex items-center gap-1 text-[var(--color-alert-danger)]">
          <AlertTriangle :size="12" /> 紧急 <span class="num-font ml-0.5">1</span>
        </div>
        <div class="flex items-center gap-1 text-[var(--color-alert-warning)]">
          <AlertTriangle :size="12" /> 重要 <span class="num-font ml-0.5">2</span>
        </div>
        <div class="flex items-center gap-1 text-gray-300">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
          一般 <span class="num-font ml-0.5 text-[var(--color-cyan-glow)]">5</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { AlertTriangle, Leaf } from 'lucide-vue-next'

// ============================================
// Clock
// ============================================
const currentTime = ref('')
let timeInterval = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', { hour12: false })
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  initMoistureChart()
})

onUnmounted(() => {
  if (timeInterval) clearInterval(timeInterval)
  if (moistureChartInstance) moistureChartInstance.dispose()
})

// ============================================
// Soil Moisture Chart (ECharts)
// ============================================
const moistureChartRef = ref(null)
let moistureChartInstance = null

const initMoistureChart = () => {
  if (!moistureChartRef.value) return
  moistureChartInstance = echarts.init(moistureChartRef.value)

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(3, 14, 22, 0.9)',
      borderColor: '#00ffcc',
      textStyle: { color: '#fff', fontSize: 12 },
      axisPointer: { type: 'line', lineStyle: { color: '#00ffcc', type: 'dashed' } }
    },
    grid: { top: '10%', left: '0%', right: '5%', bottom: '0%', containLabel: true },
    xAxis: {
      type: 'category', boundaryGap: false,
      data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
      axisLine: { lineStyle: { color: '#133c46' } },
      axisLabel: { color: '#7ab3c4', fontSize: 10, fontFamily: 'Oswald' },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value', min: 0, max: 100, splitNumber: 5,
      axisLine: { show: false },
      axisLabel: { color: '#7ab3c4', fontSize: 10, fontFamily: 'Oswald' },
      splitLine: { lineStyle: { color: '#133c46', type: 'dashed' } }
    },
    series: [{
      name: '10cm层', type: 'line', smooth: true,
      symbol: 'circle', symbolSize: 6, showSymbol: false,
      itemStyle: { color: '#00aaff' },
      lineStyle: { width: 2, color: '#00aaff' },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(0, 170, 255, 0.3)' },
          { offset: 1, color: 'rgba(0, 170, 255, 0)' }
        ])
      },
      data: [50, 55, 62, 58, 45, 32.6, 40],
    }]
  }

  moistureChartInstance.setOption(option)
}

// ============================================
// Data
// ============================================
const topStats = [
  { icon: '📦', label: '种植面积(亩)', value: '12,560' },
  { icon: '🌡️', label: '传感器数量(个)', value: '156' },
  { icon: '🛸', label: '无人机数量(台)', value: '8' },
  { icon: '⚠️', label: '告警数量(条)', value: '3', warning: true },
  { icon: '📈', label: '产量预测(kg)', value: '8,560', trend: true },
]

const nutrients = [
  { name: '有机质', value: '23.5', color: '#00ffcc' },
  { name: '氮(N)', value: '118.6', color: '#00ffcc' },
  { name: '磷(P)', value: '45.3', color: '#00ffcc' },
  { name: '钾(K)', value: '184.6', color: '#00ffcc' },
]

const bottomControls = [
  { icon: '🗺️', label: '全局视角' },
  { icon: '🌱', label: '生长模型' },
  { icon: '🔲', label: '网格管理' },
  { icon: '⚙️', label: '设备管理' },
  { icon: '📊', label: '数据图层' },
]
</script>

<style scoped>
/* Tech panel styles are inherited from global style.css */
/* Additional styles specific to open field panel */

@keyframes scan-line {
  0% { top: 0; }
  100% { top: 100%; }
}

.animate-scan-line {
  animation: scan-line 2s ease-in-out infinite alternate;
}

/* Radar scan animation */
.radar-scan {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: conic-gradient(from 0deg, transparent 70%, rgba(0, 255, 204, 0.4) 100%);
  border-radius: 50%;
  transform-origin: center;
  animation: radar-scan-anim 4s linear infinite;
}

@keyframes radar-scan-anim {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Spectrogram background */
.spectrogram-bg {
  background: linear-gradient(90deg, #010a11 0%, #052b4a 20%, #094770 40%, #1579a3 60%, #30b0b8 80%, #00ffcc 100%);
}

/* Panel styles */
.tech-panel {
  background: linear-gradient(180deg, rgba(9, 28, 40, 0.8) 0%, rgba(3, 14, 22, 0.9) 100%);
  border: 1px solid #133c46;
  position: relative;
  backdrop-filter: blur(5px);
  box-shadow: inset 0 0 20px rgba(0, 255, 204, 0.02);
  border-radius: 4px;
}

.tech-panel::before, .tech-panel::after,
.tech-panel-inner::before, .tech-panel-inner::after {
  content: ''; position: absolute; width: 10px; height: 10px; border: 2px solid transparent;
}
.tech-panel::before { top: -1px; left: -1px; border-top-color: var(--color-cyan-glow); border-left-color: var(--color-cyan-glow); }
.tech-panel::after { bottom: -1px; right: -1px; border-bottom-color: var(--color-cyan-glow); border-right-color: var(--color-cyan-glow); }
.tech-panel-inner { position: absolute; inset: 0; pointer-events: none; }
.tech-panel-inner::before { top: -1px; right: -1px; border-top-color: var(--color-cyan-glow); border-right-color: var(--color-cyan-glow); }
.tech-panel-inner::after { bottom: -1px; left: -1px; border-bottom-color: var(--color-cyan-glow); border-left-color: var(--color-cyan-glow); }

.panel-title {
  display: flex;
  align-items: center;
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 10px;
  position: relative;
  padding-left: 10px;
}
.panel-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 14px;
  background-color: var(--color-cyan-glow);
  box-shadow: 0 0 8px var(--color-cyan-glow);
}
.panel-title-line {
  flex-grow: 1;
  height: 1px;
  background: linear-gradient(90deg, rgba(0, 255, 204, 0.5), transparent);
  margin-left: 10px;
}
</style>
