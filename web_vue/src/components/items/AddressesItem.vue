<script setup lang="ts">
import type { Address } from "@/types";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Тип" :value="props.item.view" />
  <ElementLabelValue label="Адрес" :value="props.item.address" />
</template>
