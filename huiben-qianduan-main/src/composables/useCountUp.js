import { ref, onUnmounted } from 'vue'

export function useCountUp(target, options = {}) {
  const { duration = 2000, start = 0, delay = 0 } = options
  const count = ref(start)
  let rafId = null
  let started = false

  const startCount = () => {
    if (started) return
    started = true

    setTimeout(() => {
      const startTime = performance.now()
      const endValue = target

      const animate = (now) => {
        const elapsed = now - startTime
        const progress = Math.min(elapsed / duration, 1)
        // Ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3)
        count.value = Math.round(start + (endValue - start) * eased)

        if (progress < 1) {
          rafId = requestAnimationFrame(animate)
        }
      }

      rafId = requestAnimationFrame(animate)
    }, delay)
  }

  const reset = () => {
    if (rafId) cancelAnimationFrame(rafId)
    started = false
    count.value = start
  }

  onUnmounted(() => {
    if (rafId) cancelAnimationFrame(rafId)
  })

  return { count, startCount, reset }
}
