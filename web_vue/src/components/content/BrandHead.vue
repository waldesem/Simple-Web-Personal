<script setup lang="ts">
const { color1, color2 } = defineProps({
  color1: {
    type: String,
    default: 'text-blue-600',
  },
  color2: {
    type: String,
    default: 'text-red-600',
  },
});
</script>

<template>
  <div v-once class="inline-flex items-center text-xl font-bold space-x-2">
    <div :class="color1">КАДРОВАЯ</div>
    <div :class="color2">БЕЗОПАСНОСТЬ</div>
  </div>
</template>
