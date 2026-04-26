<script setup lang="ts">
import { PropType } from "vue";
import type { Staff } from "@/types";

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
