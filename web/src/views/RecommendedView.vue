<script setup lang="ts">
import { ref } from 'vue'
import { type InfoData, Units } from '@/types/InfoData.ts'
import CardDataInfo from '@/components/CardDataInfo.vue'

const recommendedData: InfoData[] = ref([
  {
    className: 'bmr',
    text: 'Your BMR',
    url: '/user/calculate/bmr',
    unit: Units.kcal,
  },
  {
    className: 'bmi',
    text: 'Your BMI',
    url: '/user/calculate/bmi',
    unit: null,
  },
])
</script>

<template>
  <CardDataInfo class-name="recommended-data" :info-datas="recommendedData" invert="invert" />
</template>

<style scoped></style>
