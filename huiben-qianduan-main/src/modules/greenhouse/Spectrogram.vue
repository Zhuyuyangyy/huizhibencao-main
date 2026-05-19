<template>
  <div class="w-full h-full relative">
    <div class="absolute top-0 left-0 text-[10px] text-gray-400 z-10">频率(Hz)</div>
    <div class="absolute bottom-[-15px] right-0 text-[10px] text-gray-400 z-10">时间(秒)</div>
    <div class="absolute left-0 top-0 bottom-0 w-6 flex flex-col justify-between text-[10px] text-gray-400 pb-4 pt-4 z-10 bg-[#021124]/50">
      <span>20k</span><span>10k</span><span>5k</span><span>2k</span><span>1k</span><span>500</span>
    </div>
    <div class="absolute bottom-0 left-6 right-0 flex justify-between text-[10px] text-gray-400 px-2">
      <span>-60</span><span>-45</span><span>-30</span><span>-15</span><span>0</span>
    </div>
    <div class="absolute top-4 left-6 right-0 bottom-4 border border-red-500/30 rounded overflow-hidden">
      <!-- Alert crosshair -->
      <div class="absolute top-[30%] right-[20%] w-8 h-8 pointer-events-none z-20">
        <div class="absolute top-1/2 left-0 right-0 h-px bg-red-500/80"></div>
        <div class="absolute left-1/2 top-0 bottom-0 w-px bg-red-500/80"></div>
        <div class="absolute inset-0 border border-red-500/80 rounded-full animate-ping opacity-50"></div>
      </div>
      <canvas ref="canvasRef" width="300" height="150" class="w-full h-full"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvasRef = ref(null)
let animationId = null

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return

  const draw = () => {
    const ctx = canvas.getContext('2d')
    const w = canvas.width
    const h = canvas.height

    ctx.fillStyle = '#050a15'
    ctx.fillRect(0, 0, w, h)

    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)'
    ctx.lineWidth = 1
    for (let i = 0; i < h; i += 20) {
      ctx.beginPath()
      ctx.moveTo(0, i)
      ctx.lineTo(w, i)
      ctx.stroke()
    }

    const barWidth = 2
    const gap = 1

    for (let x = 0; x < w; x += (barWidth + gap)) {
      const intensity = Math.sin(x / w * Math.PI) + Math.random() * 0.5
      const height = h * 0.8 * intensity * (Math.random() * 0.5 + 0.5)
      const y = h - height

      const gradient = ctx.createLinearGradient(0, h, 0, h - height)
      gradient.addColorStop(0, '#ffff00')
      gradient.addColorStop(0.3, '#ff6600')
      gradient.addColorStop(0.7, '#ff0000')
      gradient.addColorStop(1, 'rgba(255,0,0,0)')

      ctx.fillStyle = gradient
      ctx.fillRect(x, y, barWidth, height)

      if (Math.random() > 0.8) {
        ctx.fillStyle = 'rgba(255, 255, 0, 0.8)'
        ctx.fillRect(x, Math.random() * h, barWidth, 2)
      }
    }
    animationId = requestAnimationFrame(draw)
  }
  draw()
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
})
</script>
