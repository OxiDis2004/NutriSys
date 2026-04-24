<script setup lang="ts">
import { ref } from 'vue'
import type { InfoData } from '@/types/InfoData.ts'

const props = defineProps<{
  infoData: InfoData
  invert: 'normal' | 'invert'
}>()

const data = ref(0)

setTimeout(() => {
  console.log(props.infoData.url)
  data.value += 1
}, 2000)
</script>

<template>
  <div :class="[infoData.className, invert]">
    <p class="header">{{ infoData.text }}</p>
    <p class="data">{{ data }}</p>
    <p class="footer" v-if="props.infoData.unit !== null">{{ infoData.unit }}</p>
  </div>
</template>

<style scoped>
div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  font-family: 'Inter', sans-serif;
  transition:
    background-color 0.3s,
    color 0.3s;
}

p {
  resize: vertical;
  font-family: 'Inter', sans-serif;
  opacity: 1;
  margin: 0;
  line-height: 1.2;
  text-align: center;
  vertical-align: middle;
}

p.header {
  font-size: 32px;
  font-weight: normal;
  margin-bottom: 8px;
}

p.data {
  font-size: 72px;
  font-weight: bold;
  letter-spacing: -3%;
}

p.footer {
  font-size: 32px;
  font-weight: normal;
  margin-top: 8px;
  opacity: 0.6;
}

.normal {
  --header-color: var(--vt-c-text-data-header-normal);
  --data-color: var(--vt-c-text-data-data-normal);
  --footer-color: var(--vt-c-text-data-footer-normal);
}

.invert {
  --header-color: var(--vt-c-text-data-header-invert);
  --data-color: var(--vt-c-text-data-data-invert);
  --footer-color: var(--vt-c-text-data-footer-invert);
}

.header {
  color: var(--header-color);
}

.data {
  color: var(--data-color);
}

.footer {
  color: var(--footer-color);
}

@media (max-width: 776px) {
  p.header {
    font-size: 16px;
  }

  p.data {
    font-size: 36px;
  }

  p.footer {
    font-size: 16px;
  }
}

@media (max-width: 400px) {
  p.header {
    font-size: 12px;
  }

  p.data {
    font-size: 27px;
  }

  p.footer {
    font-size: 12px;
  }
}
</style>
