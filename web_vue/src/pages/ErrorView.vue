<script setup lang="ts">

const props = defineProps({
  error: {
    type: Object,
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
