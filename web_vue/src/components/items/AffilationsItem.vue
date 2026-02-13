<script setup lang="ts">
import type { Affilation } from "@/types";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Тип участия" :value="props.item.view" />
  <LabelValue label="Организация" :value="props.item.organization" />
  <LabelValue label="ИНН" :value="props.item.inn" />
</template>
