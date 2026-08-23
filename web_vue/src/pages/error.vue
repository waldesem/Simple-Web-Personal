<script setup lang="ts">
const { code, status, message } = defineProps({
  code: { type: String, required: true },
  status: { type: [String], required: true },
  message: { type: [Object, String], required: true },
});
</script>

<template>
  <UPageCard class="w-full max-w-md m-auto my-[20vh]">
    <UError
      :error="{
        statusCode: code,
        statusMessage: status,
        message: message,
      }"
    />
  </UPageCard>
</template>
