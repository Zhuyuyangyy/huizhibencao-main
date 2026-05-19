<template>
  <div class="flex gap-3 items-center">
    <div class="flex-1 relative h-20 rounded border border-[var(--color-border)] overflow-hidden">
      <canvas ref="canvasRef" class="w-full h-full" width="300" height="80"></canvas>
    </div>
    <div class="w-[120px] flex items-center gap-3 shrink-0">
      <div class="flex items-center gap-1">
        <div class="w-1.5 h-16 bg-gradient-to-b from-red-500 via-yellow-400 to-green-600 rounded"></div>
        <div class="flex flex-col justify-between h-16 text-[10px] text-gray-400 py-0.5">
          <span>1.0</span>
          <span>0.5</span>
          <span>0</span>
        </div>
      </div>
      <div class="flex flex-col justify-center">
        <span class="text-[10px] text-gray-400 mb-1">当前NDVI均值</span>
        <div class="text-2xl font-bold text-white flex items-baseline gap-1">
          0.78 <span class="text-[var(--color-cyan-glow)] text-sm">↑</span>
        </div>
        <span class="text-[10px] text-gray-400">较昨日 <span class="text-[var(--color-cyan-glow)]">+0.05</span></span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const canvasRef = ref(null)

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w = canvas.width
  const h = canvas.height

  ctx.fillStyle = '#0a5c0a'
  ctx.fillRect(0, 0, w, h)

  const drawBlob = (color, count, minR, maxR) => {
    for (let i = 0; i < count; i++) {
      const x = Math.random() * w
      const y = Math.random() * h
      const r = minR + Math.random() * (maxR - minR)
      const grad = ctx.createRadialGradient(x, y, 0, x, y, r)
      grad.addColorStop(0, color)
      grad.addColorStop(1, 'transparent')
      ctx.fillStyle = grad
      ctx.beginPath()
      ctx.arc(x, y, r, 0, Math.PI * 2)
      ctx.fill()
    }
  }

  drawBlob('rgba(0, 220, 0, 0.8)', 30, 10, 25)
  drawBlob('rgba(200, 255, 0, 0.8)', 20, 8, 20)
  drawBlob('rgba(255, 150, 0, 0.85)', 15, 8, 18)
  drawBlob('rgba(255, 0, 0, 0.9)', 10, 5, 15)
})
</script>
