<script setup lang="ts">
import type { NuxtError } from "nuxt/app";

const props = defineProps({
  error: {
    type: Object as () => NuxtError,
    required: true,
  },
});
</script>

<template>
  <UError
    :error="{
      statusCode: props.error.statusCode,
      statusMessage: props.error.statusMessage,
      message: props.error.message,
    }"
  />
</template>
