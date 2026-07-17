<script setup lang="ts">
const props = defineProps({
  animated: {
    type: Boolean,
    default: false,
  },
  size: {
    type: String,
    default: "text-xl",
  },
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
  <div
    :class="[{ heading: props.animated }, props.size]"
    class="inline-flex items-center font-bold space-x-2"
  >
    <div :class="props.color1">КАДРОВАЯ</div>
    <div :class="props.color2">БЕЗОПАСНОСТЬ</div>
  </div>
</template>

<style scoped>
.heading {
  animation: rotate 3s infinite ease 0.5s;
}

@keyframes rotate {
  from {
    transform: rotateX(0deg);
  }
  to {
    transform: rotateX(360deg);
  }
}
</style>
