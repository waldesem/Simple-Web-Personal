<script setup lang="ts">
import type { Education } from "@/types";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Уровень образования" :value="props.item.view" />
  <LabelValue label="Учебное заведение" :value="props.item.institution" />
  <LabelValue
    v-if="props.item.finished"
    label="Год окончания"
    :value="props.item.finished"
  />
  <LabelValue label="Специальность" :value="props.item.specialty" />
</template>
