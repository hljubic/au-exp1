<template>
  <div class="min-h-screen bg-slate-100 text-slate-800">
    <header class="border-b border-slate-200 bg-white">
      <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
            Analitika učenja
          </p>
          <h1 class="text-lg font-semibold text-slate-900">
            Students Performance Dashboard
          </h1>
        </div>

        <nav class="flex items-center gap-2">
          <router-link
            v-for="link in links"
            :key="link.link"
            :to="link.link"
            class="rounded-lg px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
            active-class="bg-slate-900 text-white hover:bg-slate-900 hover:text-white"
          >
            {{ link.text }}
          </router-link>
        </nav>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-4 py-6">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
const links = [
  { text: 'Početna', link: '/' },
  { text: 'Grafikoni', link: '/charts' },
  { text: 'Predikcija', link: '/predict' },
]
</script>
