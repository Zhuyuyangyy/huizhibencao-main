<template>
  <div class="w-full h-full">
    <Radar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Radar } from 'vue-chartjs'
import { radarData } from '@/composables/useSensorData'

const chartData = computed(() => ({
  labels: radarData.map(d => d.subject),
  datasets: [
    {
      label: '环境数据',
      data: radarData.map(d => (d.A / d.fullMark) * 100),
      backgroundColor: 'rgba(0, 255, 255, 0.25)',
      borderColor: '#00ffff',
      borderWidth: 2.5,
      pointBackgroundColor: '#00ffff',
      pointBorderColor: '#01060e',
      pointBorderWidth: 2,
      pointRadius: 4,
      pointHoverRadius: 6,
      fill: true,
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      angleLines: { color: 'rgba(0, 255, 255, 0.15)', lineWidth: 1 },
      grid: { color: 'rgba(0, 255, 255, 0.1)', circular: true },
      pointLabels: { color: '#a0aec0', font: { size: 11, weight: '500' }, padding: 12 },
      ticks: { display: false, stepSize: 20 },
      min: 0,
      max: 100,
      beginAtZero: true,
    }
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(2, 17, 36, 0.95)',
      borderColor: '#00ffff',
      borderWidth: 1,
      titleColor: '#fff',
      bodyColor: '#00ffff',
      padding: 12,
      cornerRadius: 8,
      displayColors: false,
      callbacks: {
        label: function(context) {
          const item = radarData[context.dataIndex]
          return `${item.A}${item.unit || ''} (${Math.round((item.A / item.fullMark) * 100)}%)`
        }
      }
    }
  },
  interaction: { intersect: false, mode: 'index' }
}
</script>
