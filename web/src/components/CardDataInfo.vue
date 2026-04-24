<script setup lang="ts">
import DataShow from '@/components/DataShow.vue'
import type { InfoData } from '@/types/InfoData'

const props = defineProps<{
  className: string
  infoDatas: InfoData[]
  invert: 'normal' | 'invert'
}>()

console.log(props.infoDatas)
</script>

<template>
  <div class="container-data" :class="invert">
    <div v-for="(infoData, index) in infoDatas" :key="index" :class="className + '-' + index">
      <DataShow :info-data="infoData" :invert="invert" />
    </div>
  </div>
</template>

<style scoped>
.container-data {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-content: center;
  gap: 4em;
  width: 100%;
}

.normal {
  background-color: var(--vt-bg-data-normal);
}

.invert {
  background-color: var(--vt-bg-data-invert);
}

@media (max-width: 768px) {
  .container-data {
    gap: 0;
  }
}
</style>
