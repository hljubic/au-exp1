<template>
  <div class="space-y-6">
    <section class="rounded-2xl bg-white p-6 shadow-sm">
      <div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p class="text-sm font-medium text-slate-500">Vizualizacija</p>
          <h2 class="text-3xl font-semibold text-slate-900">
            Grafikoni nad students datasetom
          </h2>
        </div>
        <p class="max-w-2xl text-sm text-slate-500">
          Ovdje su prikazani različiti tipovi grafikona preko Chart.js biblioteke:
          bar, doughnut, radar i scatter.
        </p>
      </div>
    </section>

    <div
      v-if="loading"
      class="rounded-2xl bg-white p-6 text-sm text-slate-500 shadow-sm"
    >
      Učitavanje grafikona...
    </div>

    <div
      v-else-if="error"
      class="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-600 shadow-sm"
    >
      {{ error }}
    </div>

    <template v-else>
      <section class="grid gap-6 md:grid-cols-3">
        <div class="rounded-2xl bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-slate-900">Prosjeci rezultata</h3>
          <canvas ref="scoreMeansCanvas"></canvas>
        </div>

        <div class="rounded-2xl bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-slate-900">Distribucija po spolu</h3>
          <canvas ref="genderCanvas"></canvas>
        </div>

        <div class="rounded-2xl bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-slate-900">Prosjeci prema lunch tipu</h3>
          <canvas ref="lunchCanvas"></canvas>
        </div>

        <div class="rounded-2xl bg-white p-6 shadow-sm md:col-span-2">
          <h3 class="mb-4 text-lg font-semibold text-slate-900">Math score vs Writing score</h3>
          <canvas ref="scatterCanvas"></canvas>
        </div>

        <div class="rounded-2xl bg-white p-6 shadow-sm">
          <h3 class="mb-4 text-lg font-semibold text-slate-900">Race / ethnicity raspodjela</h3>
          <canvas ref="raceCanvas"></canvas>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { Chart } from 'chart.js/auto'
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

interface SimpleChartData {
  labels: string[]
  values: number[]
}

interface LunchChartData {
  labels: string[]
  datasets: Array<{
    label: string
    values: number[]
  }>
}

interface ScatterPoint {
  x: number
  y: number
}

interface ChartsResponse {
  score_means: SimpleChartData
  gender_counts: SimpleChartData
  race_counts: SimpleChartData
  lunch_score_means: LunchChartData
  math_vs_writing: ScatterPoint[]
}

const loading = ref(true)
const error = ref('')
const chartData = ref<ChartsResponse | null>(null)

const scoreMeansCanvas = ref<HTMLCanvasElement | null>(null)
const genderCanvas = ref<HTMLCanvasElement | null>(null)
const lunchCanvas = ref<HTMLCanvasElement | null>(null)
const scatterCanvas = ref<HTMLCanvasElement | null>(null)
const raceCanvas = ref<HTMLCanvasElement | null>(null)

const chartInstances: Chart[] = []

const destroyCharts = () => {
  chartInstances.forEach((chart) => chart.destroy())
  chartInstances.length = 0
}

const buildCharts = () => {
  if (!chartData.value) {
    return
  }

  destroyCharts()

  if (scoreMeansCanvas.value) {
    chartInstances.push(new Chart(scoreMeansCanvas.value, {
      type: 'bar',
      data: {
        labels: chartData.value.score_means.labels,
        datasets: [{
          label: 'Prosječna vrijednost',
          data: chartData.value.score_means.values,
          backgroundColor: ['#2563eb', '#0f766e', '#d97706'],
          borderRadius: 8,
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
      },
    }))
  }

  if (genderCanvas.value) {
    chartInstances.push(new Chart(genderCanvas.value, {
      type: 'doughnut',
      data: {
        labels: chartData.value.gender_counts.labels,
        datasets: [{
          data: chartData.value.gender_counts.values,
          backgroundColor: ['#8b5cf6', '#06b6d4'],
        }],
      },
      options: {
        responsive: true,
      },
    }))
  }

  if (lunchCanvas.value) {
    chartInstances.push(new Chart(lunchCanvas.value, {
      type: 'radar',
      data: {
        labels: chartData.value.lunch_score_means.labels,
        datasets: chartData.value.lunch_score_means.datasets.map((dataset, index) => ({
          label: dataset.label,
          data: dataset.values,
          backgroundColor: index === 0 ? 'rgba(37, 99, 235, 0.2)' : 'rgba(217, 119, 6, 0.2)',
          borderColor: index === 0 ? '#2563eb' : '#d97706',
          pointBackgroundColor: index === 0 ? '#2563eb' : '#d97706',
        })),
      },
      options: {
        responsive: true,
      },
    }))
  }

  if (scatterCanvas.value) {
    chartInstances.push(new Chart(scatterCanvas.value, {
      type: 'scatter',
      data: {
        datasets: [{
          label: 'Students',
          data: chartData.value.math_vs_writing,
          backgroundColor: '#0f766e',
        }],
      },
      options: {
        responsive: true,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Math score',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Writing score',
            },
          },
        },
      },
    }))
  }

  if (raceCanvas.value) {
    chartInstances.push(new Chart(raceCanvas.value, {
      type: 'polarArea',
      data: {
        labels: chartData.value.race_counts.labels,
        datasets: [{
          data: chartData.value.race_counts.values,
          backgroundColor: ['#2563eb', '#7c3aed', '#db2777', '#0f766e', '#d97706'],
        }],
      },
      options: {
        responsive: true,
      },
    }))
  }
}

const loadCharts = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/charts')

    if (!response.ok) {
      throw new Error('Neuspješno dohvaćanje chart podataka.')
    }

    chartData.value = await response.json()
    loading.value = false
    await nextTick()
    buildCharts()
  } catch (err) {
    console.error(err)
    error.value = 'Backend nije dostupan ili nije moguće nacrtati grafikone.'
  } finally {
    if (chartData.value === null) {
      loading.value = false
    }
  }
}

onMounted(loadCharts)
onBeforeUnmount(destroyCharts)
</script>
