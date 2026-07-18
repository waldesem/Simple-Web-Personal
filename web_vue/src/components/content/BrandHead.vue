<script setup lang="ts">
const props = defineProps({
  color1: {
    type: String,
    default: "text-blue-600",
  },
  color2: {
    type: String,
    default: "text-red-600",
  },
});
</script>

<template>
  <div class="inline-flex items-center text-xl font-bold space-x-2">
    <div :class="props.color1">КАДРОВАЯ</div>
    <div :class="props.color2">БЕЗОПАСНОСТЬ</div>
  </div>
</template>
