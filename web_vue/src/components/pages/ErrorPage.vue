<script setup lang="ts">
import { PropType } from "vue";

interface CustomError {
  statusCode: number;
  statusMessage: string;
}

const props = defineProps({
  error: {
    type: Object as PropType<CustomError>,
    default: {
      statusCode: 404,
      statusMessage: "Not found",
    },
  },
});
</script>

<template>
  <NUContainer>
    <NUError :error="props.error" />
  </NUContainer>
</template>
