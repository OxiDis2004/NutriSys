<script setup lang="ts">
import { type InfoData, Units } from '@/types/InfoData.ts'
import { ref } from 'vue'
import CardDataInfo from '@/components/CardDataInfo.vue'

const dailyStatisticData: InfoData[] = ref([
  {
    className: 'calorie',
    text: 'You ate today',
    url: '/food/statistic/day',
    unit: Units.kcal,
  },
  {
    className: 'water',
    text: 'You drunk today',
    url: '/water/statistic/day',
    unit: Units.Liter,
  },
])
</script>

<template>
  <CardDataInfo class-name="daily-statistic" :info-datas="dailyStatisticData" invert="normal"/>
</template>

<style scoped></style>
