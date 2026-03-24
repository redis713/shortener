<template>
  <div class="container">
    <h1>URL Shortener</h1>

    <div class="input-group">
      <input v-model="url" placeholder="https://example.com" />
      <button @click="shorten">Shorten</button>
    </div>

    <p v-if="shortLink" style="margin-top: 20px;">
      → <a :href="shortLink" target="_blank">{{ shortLink }}</a>
    </p>
  </div>
</template>


<script setup>
import { ref } from 'vue'

const url = ref('')
const shortLink = ref('')

async function shorten() {
  const res = await fetch('/api/shorten', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      original_url: url.value
    })
  })

  const data = await res.json()

  shortLink.value = `http://192.168.1.20/${data.short_code}`
}
</script>
