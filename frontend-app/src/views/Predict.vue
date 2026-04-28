<template>
  <div class="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
    <section class="rounded-2xl bg-white p-6 shadow-sm">
      <p class="text-sm font-medium text-slate-500">Predikcija</p>
      <h2 class="mt-1 text-3xl font-semibold text-slate-900">
        Predviđanje writing score
      </h2>
      <p class="mt-3 text-sm text-slate-500">
        Forma koristi isti skup ulaznih varijabli na kojima je model treniran u notebooku.
      </p>

      <form class="mt-6 space-y-4" @submit.prevent="submitForm">
        <div>
          <label class="mb-1 block text-sm font-medium text-slate-700">Gender</label>
          <select
            v-model="form.gender"
            required
            class="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-slate-800 outline-none transition focus:border-slate-400"
          >
            <option value="">Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-slate-700">
            Race / Ethnicity
          </label>
          <select
            v-model="form['race/ethnicity']"
            required
            class="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-slate-800 outline-none transition focus:border-slate-400"
          >
            <option value="">Select group</option>
            <option value="group A">Group A</option>
            <option value="group B">Group B</option>
            <option value="group C">Group C</option>
            <option value="group D">Group D</option>
            <option value="group E">Group E</option>
          </select>
        </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-slate-700">
            Math Score
          </label>
          <input
            v-model.number="form['math score']"
            type="number"
            min="0"
            max="100"
            required
            class="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-slate-800 outline-none transition focus:border-slate-400"
          />
        </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-slate-700">
            Reading Score
          </label>
          <input
            v-model.number="form['reading score']"
            type="number"
            min="0"
            max="100"
            required
            class="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-slate-800 outline-none transition focus:border-slate-400"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white transition hover:bg-slate-800 disabled:bg-slate-400"
        >
          {{ loading ? 'Predicting...' : 'Predict' }}
        </button>
      </form>
    </section>

    <section class="rounded-2xl bg-white p-6 shadow-sm">
      <h3 class="text-lg font-semibold text-slate-900">Rezultat</h3>
      <div class="mt-4 rounded-2xl bg-slate-50 p-6">
        <p class="text-sm text-slate-500">Predicted writing score</p>
        <p class="mt-2 text-5xl font-semibold text-slate-900">
          {{ prediction ?? '--' }}
        </p>
      </div>

      <div
        v-if="errorMessage"
        class="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600"
      >
        {{ errorMessage }}
      </div>

      <div class="mt-6 rounded-2xl border border-slate-200 p-5">
        <p class="text-sm font-semibold text-slate-800">Napomena</p>
        <p class="mt-2 text-sm text-slate-500">
          Model koristi samo četiri ulaza: <code>gender</code>, <code>race/ethnicity</code>,
          <code>math score</code> i <code>reading score</code>.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'

interface PredictionForm {
  gender: string
  'race/ethnicity': string
  'math score': number | null
  'reading score': number | null
}

const form = reactive<PredictionForm>({
  gender: '',
  'race/ethnicity': '',
  'math score': null,
  'reading score': null,
})

const prediction = ref<number | null>(null)
const loading = ref(false)
const errorMessage = ref('')

const submitForm = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || 'Request failed')
    }

    prediction.value = data.predicted_writing_score
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Greška kod slanja zahtjeva na API.'
  } finally {
    loading.value = false
  }
}
</script>
