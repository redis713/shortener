<template>
  <div class="container">
    <h1>Links</h1>

    <table>
      <thead>
        <tr>
          <th>Short</th>
          <th>Original</th>
          <th>Clicks</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="url in urls" :key="url.short_code">
          <td>
            <a :href="getUrl(url.short_code)" target="_blank">
              {{ url.short_code }}
            </a>
          </td>
          <td>{{ url.original_url }}</td>
          <td>{{ url.clicks }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'

const urls = ref([])

const baseUrl = window.location.origin
const getUrl = (code) => `${baseUrl}/${code}`

onMounted(async () => {
  const res = await fetch('/api/urls')
  const data = await res.json()
  urls.value = data.urls
})
</script>
