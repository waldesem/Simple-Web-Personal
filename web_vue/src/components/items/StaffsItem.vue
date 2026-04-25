<script setup lang="ts">
import type { Staff } from "@/types";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Должность" :value="props.item.position" />
  <LabelValue label="Департамент" :value="props.item.department" />
</template>
