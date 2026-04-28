<template>
  <div class="space-y-6">
    <section class="rounded-2xl bg-white p-6 shadow-sm">
      <div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p class="text-sm font-medium text-slate-500">Početna analiza</p>
          <h2 class="text-3xl font-semibold text-slate-900">
            Pregled dataseta i deskriptivna statistika
          </h2>
        </div>
        <p class="max-w-2xl text-sm text-slate-500">
          Ova stranica prikazuje osnovne informacije o datasetu, nedostajuće vrijednosti,
          deskriptivnu statistiku i nekoliko kratkih insighta iz podataka.
        </p>
      </div>
    </section>

    <div
      v-if="loading"
      class="rounded-2xl bg-white p-6 text-sm text-slate-500 shadow-sm"
    >
      Učitavanje podataka...
    </div>

    <div
      v-else-if="error"
      class="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-600 shadow-sm"
    >
      {{ error }}
    </div>

    <template v-else-if="overview">
      <section class="grid gap-4 md:grid-cols-4">
        <div class="rounded-2xl bg-white p-5 shadow-sm">
          <p class="text-sm text-slate-500">Originalni retci</p>
          <p class="mt-2 text-3xl font-semibold text-slate-900">
            {{ overview.dataset.rows_original }}
          </p>
        </div>
        <div class="rounded-2xl bg-white p-5 shadow-sm">
          <p class="text-sm text-slate-500">Stupci</p>
          <p class="mt-2 text-3xl font-semibold text-slate-900">
            {{ overview.dataset.cols_original }}
          </p>
        </div>
        <div class="rounded-2xl bg-white p-5 shadow-sm">
          <p class="text-sm text-slate-500">Čisti retci</p>
          <p class="mt-2 text-3xl font-semibold text-slate-900">
            {{ overview.dataset.rows_clean }}
          </p>
        </div>
        <div class="rounded-2xl bg-white p-5 shadow-sm">
          <p class="text-sm text-slate-500">Uklonjeni retci</p>
          <p class="mt-2 text-3xl font-semibold text-slate-900">
            {{ overview.dataset.rows_original - overview.dataset.rows_clean }}
          </p>
        </div>
      </section>

      <section class="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div class="rounded-2xl bg-white p-6 shadow-sm">
          <h3 class="text-lg font-semibold text-slate-900">Opis dataseta</h3>
          <div class="mt-4 overflow-x-auto">
            <table class="min-w-full text-sm">
              <thead>
                <tr class="border-b border-slate-200 text-left text-slate-500">
                  <th class="pb-3 pr-4 font-medium">Polje</th>
                  <th class="pb-3 pr-4 font-medium">Vrijednost</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="column in overview.dataset.column_names"
                  :key="column"
                  class="border-b border-slate-100"
                >
                  <td class="py-3 pr-4 font-medium text-slate-700">{{ column }}</td>
                  <td class="py-3 pr-4 text-slate-500">
                    {{ overview.missing_values[column] }} missing vrijednosti
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="rounded-2xl bg-white p-6 shadow-sm">
          <h3 class="text-lg font-semibold text-slate-900">Zanimljivi insights</h3>
          <div class="mt-4 space-y-3">
            <div
              v-for="insight in overview.insights"
              :key="insight.title"
              class="rounded-xl bg-slate-50 p-4"
            >
              <p class="text-sm font-semibold text-slate-800">{{ insight.title }}</p>
              <p class="mt-1 text-sm text-slate-500">{{ insight.value }}</p>
            </div>
          </div>
        </div>
      </section>

      <section class="rounded-2xl bg-white p-6 shadow-sm">
        <h3 class="text-lg font-semibold text-slate-900">Deskriptivna statistika</h3>
        <div class="mt-4 overflow-x-auto">
          <table class="min-w-full text-sm">
            <thead>
              <tr class="border-b border-slate-200 text-left text-slate-500">
                <th class="pb-3 pr-4 font-medium">Metrika</th>
                <th class="pb-3 pr-4 font-medium">Math score</th>
                <th class="pb-3 pr-4 font-medium">Reading score</th>
                <th class="pb-3 pr-4 font-medium">Writing score</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in overview.descriptive_statistics"
                :key="row.metric"
                class="border-b border-slate-100"
              >
                <td class="py-3 pr-4 font-medium text-slate-700">{{ row.metric }}</td>
                <td class="py-3 pr-4 text-slate-500">{{ row['math score'] }}</td>
                <td class="py-3 pr-4 text-slate-500">{{ row['reading score'] }}</td>
                <td class="py-3 pr-4 text-slate-500">{{ row['writing score'] }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

interface DescriptiveRow {
  metric: string
  'math score': number
  'reading score': number
  'writing score': number
}

interface Insight {
  title: string
  value: string
}

interface OverviewResponse {
  dataset: {
    rows_original: number
    cols_original: number
    rows_clean: number
    cols_clean: number
    column_names: string[]
  }
  missing_values: Record<string, number>
  descriptive_statistics: DescriptiveRow[]
  insights: Insight[]
}

const overview = ref<OverviewResponse | null>(null)
const loading = ref(true)
const error = ref('')

const loadOverview = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/overview')

    if (!response.ok) {
      throw new Error('Neuspješno dohvaćanje overview podataka.')
    }

    overview.value = await response.json()
  } catch (err) {
    console.error(err)
    error.value = 'Backend nije dostupan ili je došlo do greške pri dohvaćanju podataka.'
  } finally {
    loading.value = false
  }
}

onMounted(loadOverview)
</script>
